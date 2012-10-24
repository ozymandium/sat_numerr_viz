#!/usr/bin/python
"""
Rendering in the visualizer. This is the workhorse of picture-making..

"""
import sys
import pdb
from PySide import QtCore
from PySide import QtGui
from PySide import QtNetwork
import ptolemy
from pprint import pprint
from time import sleep
from math import radians
from math import degrees
import numpy as np



class RendThread(QtCore.QThread):
    """Thread for the LFviz RenderArea"""
    def run():
        """reimplement run()"""
        socket = QtNetwork.QTcpSocket()
        socket.connectToHost('127.0.0.1', 9002)
        self.exec_()


class RenderArea(QtGui.QWidget):
    """Render area for rendering the leader and follower, etc."""
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mw = None # allow accessing data in the main window later
        self.thread = RendThread()

        ### Config ###
        self.scale_sizefrac = .5 # what fraction of the height to use for scale
        self.rgb_states = dict([['green', (0, 255, 0)], \
                                ['red', (255, 0, 0)]])
        self.scale_bg_color = QtCore.Qt.white
        
        # Declare state variables
        self.color = 'red'
        self.onesat_pix = 0.0
        self.scaleHt = 0.0
        self.scaleIncs = np.array([])
        self.numx_offset = 1
        self.numy_offset = 1
             
        print('RenderArea intialized')

    ### Painter Functions ###s
    def paintEvent(self, event):
        """Reimplementation
        Handles painting in the render area
        This function should be a delegator and obtain timestep data only
        """
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.black)) 
        
        self.getDataSnapshot()

        self.drawScale(painter)

        painter.save()
        self.drawIndicator(painter)
        painter.restore()

        painter.end()


    def getDataSnapshot(self):
        """"""
        self.renderWd = self.size().width() 
        self.renderHt = self.size().height() 
        self.onesat_pix = self.renderWd / self.mw.numsat_max
        self.scaleHt = self.renderHt*self.scale_sizefrac
        self.scaleIncs = np.arange(1, 
                            self.mw.numsat_max*self.onesat_pix+self.onesat_pix, 
                            self.onesat_pix)


    def drawScale(self, painter):
        """draw numbers and tick marks"""
        # Draw a white background
        painter.fillRect(0, 0, self.renderWd, self.scaleHt, self.scale_bg_color)
        
        tickpen = QtGui.QPen()
        tickpen.setColor(QtCore.Qt.gray)
        tickpen.setWidthF(2)

        ## Tick Number Font Settings
        tickFont = self.font()
        font_pix = 11
        tickFont.setPixelSize(font_pix)
        self.setFont(tickFont)
        fontMetrics = QtGui.QFontMetrics(tickFont)
        self.xFontBoundingRect = fontMetrics.boundingRect(self.tr("x"))
        self.yFontBoundingRect = fontMetrics.boundingRect(self.tr("y"))
        htmlSpec = ''.join(['<p style="color: black; font: ', str(font_pix), 'px;">'])
        text_doc = QtGui.QTextDocument()

        num = int(0)
        for x in self.scaleIncs:
            # Draw Major Ticks
            painter.save()
            painter.setPen(tickpen)
            painter.drawLine(x, self.scaleHt*2/3, x, self.scaleHt)
            painter.restore()

            # Draw numbers
            painter.save()
            html = ''.join([htmlSpec, str(num), '</p>'])

            painter.translate(x-4, 0)
            text_doc.setHtml(html)
            text_doc.drawContents(painter)
            painter.restore()

            num += int(1)


    def drawIndicator(self, painter):
        """draw the actual color bar"""
        self.mw.numsat = int(input('number of satellites? '))
        if self.mw.numsat > self.mw.numsat_critical:
            painter.fillRect(0, self.scaleHt,
                             self.mw.numsat*self.onesat_pix, self.renderHt-self.scaleHt,
                             QtCore.Qt.green)
        else:
            painter.fillRect(0, self.scaleHt,
                             self.mw.numsat*self.onesat_pix, self.renderHt-self.scaleHt,
                             QtCore.Qt.red)



if __name__ == '__main__':
    raise Exception('Do not import this module directly')
