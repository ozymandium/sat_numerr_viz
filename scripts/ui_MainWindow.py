# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Oct 23 20:55:57 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(432, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../graphics/gavlab_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.numsat_label = QtGui.QLabel(self.centralwidget)
        self.numsat_label.setGeometry(QtCore.QRect(0, 30, 151, 21))
        self.numsat_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.numsat_label.setObjectName("numsat_label")
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(150, 110, 280, 80))
        self.lcdNumber.setFrameShape(QtGui.QFrame.WinPanel)
        self.lcdNumber.setFrameShadow(QtGui.QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(7, 90, 421, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.err_label = QtGui.QLabel(self.centralwidget)
        self.err_label.setGeometry(QtCore.QRect(0, 140, 111, 16))
        self.err_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.err_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.err_label.setObjectName("err_label")
        self.render_area = RenderArea(self.centralwidget)
        self.render_area.setGeometry(QtCore.QRect(150, 0, 280, 90))
        self.render_area.setMinimumSize(QtCore.QSize(10, 10))
        self.render_area.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.render_area.setStyleSheet("background: rgb(0, 0, 0);")
        self.render_area.setObjectName("render_area")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GPS Status", None, QtGui.QApplication.UnicodeUTF8))
        self.numsat_label.setText(QtGui.QApplication.translate("MainWindow", "Connected Satellites", None, QtGui.QApplication.UnicodeUTF8))
        self.err_label.setText(QtGui.QApplication.translate("MainWindow", "Error Value (m)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

from renderarea import RenderArea
