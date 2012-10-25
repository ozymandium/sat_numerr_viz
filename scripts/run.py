#!/usr/bin/env python
"""
Copyright 2012 by Robert Cofield, for GAVLab. All rights reserved.

Master runner file.
Execute from within the scripts/ folder
"""
from numerrViz import MainWindow
from moos import MoosWidget
from yaml import load
from PySide import QtGui
import sys, os
from ui_MainWindow import Ui_MainWindow


### Settings ###
navpy_location = '/home/rgcofield/devel/sat_numerr_viz_ws/'
moos_config_file = '/home/rgcofield/devel/sat_numerr_viz_ws/sat_numerr_viz/cfg/moos.yaml'
################

sys.path.append(navpy_location)

moos_stream = file(moos_config_file, 'r')
moos_config = load(moos_stream)


def main():
    # MOOS
    os.system("gnome-terminal -x 'MOOSDB'")
    os.system("gnome-terminal -x 'uPlayBack'")

    #Setup QtApp
    app = QtGui.QApplication(sys.argv[0])
    ui_mainwindow = Ui_MainWindow()

    #Setup Moos App
    moos_widget = MoosWidget(moos_config)

    #Setup primary app, feed it the main window and configuration.
    #Bring up mainwindow and enter main loop
    main_window = MainWindow(ui_mainwindow)
    main_window.show()

    # Connect Signals/Slots
    moos_widget.num_updated.connect(main_window.onNum_upd)
    moos_widget.err_updated.connect(main_window.onErr_upd)

    try:
        sys.exit(app.exec_())
    except:
        x = os.system('killall uPlayBack')
        y = os.system('killall MOOSDB')
        sys.exit()


if __name__ == '__main__':
    main()
