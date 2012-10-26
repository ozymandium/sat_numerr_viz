#!/usr/bin/env python
"""
Copyright (C) 2012 Robert Cofield, for GAVLab, Auburn University.
All rights reserved.

This file is part of the Leader/Follower GUI. It is the master file.

Python v2.7.3
PySide v1.1.0
MOOS r.2354

currently this file must be executed from within the scripts folder
"""
import sys
import os
import fileinput
from yaml import load
from time import sleep
from pprint import pprint as pp
import pdb
from copy import deepcopy as dcp
from math import degrees
from math import atan2
from collections import deque
import ptolemy
import renderarea
from PySide import QtCore
from PySide import QtGui
from PySide import QtNetwork
from ui_MainWindow import Ui_MainWindow


class VizThread(QtCore.QThread):
    """Thread for the LFviz MainWindow"""
    this_ip = '127.0.0.1'
    this_port = 9001

    def run():
        """reimplement run()"""
        socket = QtNetwork.QTcpSocket()
        socket.connectToHost(VizThread.this_ip, VizThread.this_port)
        self.exec_()


class MainWindow(QtGui.QMainWindow):
    """ This is the implementation of the generated UI of the MainWindow
        It has a MOOS dataflow structure
    """
    
    def __init__(self, ui):
        ### Qt init ###
        QtGui.QMainWindow.__init__(self)
        self.ui = ui
        self.thread = VizThread()
        print('MainWindow initialized')
        self.ui.setupUi(self)
        # give renderarea a reference to me
        self.ui.render_area.mw = self

        ### Config
        self.numsat_critical = 3
        self.numsat_warning = 4
        self.numsat_max = 14

        ### Initialize display value s
        self.err = float(0.0)
        self.numsat = int(0)
        

    # ##### Functions to receive updates from moos #####
    @QtCore.Slot(int)
    def onNum_upd(self, num):
        """   update the number of satellites - receive from moos    """
        self.numsat = num
        self.ui.render_area.update()
    
    @QtCore.Slot(float)
    def onErr_upd(self, err):
        """
        Handles new relative (to follower) points for path
        updates distance and lat dev
        """
        pass
        self.ui.lcdNumber.display(err)
    #     # print('In LFviz.onPath_upd')
    #     self.pathENU = path # will be converted to render area coords by ptolemy function, invoked by renderarea on paint event
    #     self.ui.render_area.update()
    #     self.ui.dstDisp_lcd.display(self.dst)
    #     self.dev = ptolemy.getLatDev(self)
    #     self.ui.devDisp_lcd.display(self.dev)

    #     # Get leader course from it's last vs current position
    #     self.lcrsENU = ptolemy.calcENUcourse2(self.lposENU[0], self.lposENU[1],\
    #                                           self.pathENU[0][0], self.pathENU[0][1])
    #     self.lposENU = self.pathENU[0]
    #     self.ui.render_area.update()

################################################################################
if __name__ == '__main__':
    raise Exception('Do not run this file directly')
    