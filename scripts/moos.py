#!/usr/bin/env python
"""
Implementation of the pyMOOS MOOSCommClient
"""
import sys
from pymoos.MOOSCommClient import MOOSCommClient
import ptolemy
from pprint import pprint as pp
from PySide import QtGui
from PySide import QtCore
from time import sleep
import pdb


class MoosThread(QtCore.QThread):
    """Thread for the MOOSCommClient"""
    this_ip = '127.0.0.1'
    this_port = 9000

    def run():
        """reimplement run()"""
        socket = QtNetwork.QTcpSocket()
        socket.connectToHost(MoosThread.this_ip, MoosThread.this_port)
        self.exec_()


class MoosWidget(QtGui.QWidget):
    """
    Qt implementation of the MOOSCommClient
    """
    num_updated = QtCore.Signal(int)
    err_updated = QtCore.Signal(float)

    def __init__(self, config, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.thread = MoosThread()
        self.desired_variables = config['desired_variables']
        
        self.moos_client = MOOSCommClient()
        self.moos_client.SetOnConnectCallBack(self.onConnect)
        self.moos_client.SetOnMailCallBack(self.onMail)
        self.moos_client.Run(self.thread.this_ip, self.thread.this_port, \
                             'sat_numerr_viz', 50)
        # Check Connection
        for x in range(30):
            sleep(0.1)
            if self.moos_client.IsConnected():
                print("\nConnected to MOOSDB")
                break
        if not self.moos_client.IsConnected():
            print("MOOSCommClient Error:: Failed to Connect to MOOSDB")
            sys.exit(-1)

        self.err_holder = {}

    ### Primary MOOS Functions ###
    def onConnect(self):
        """MOOS callback - required in every MOOS app's class definition"""
        print('In MoosWidget.onConnect :: waiting for mail..')
        for var in self.desired_variables:
            self.moos_client.Register(var)
        return

    def onMail(self):
        """MOOS callback - required in every MOOS app's class definition"""
        print('\n--- In MoosWidget.onMail :: Retrieving inbox contents ---')
        for message in self.moos_client.FetchRecentMail():
            self.unpack_msg(message)
        return True


    ### Mail handling functions ###
    def unpack_msg(self, msg):
        """parse moos messages. put into dictionary
        handles conversion of any strings
        """
        print('\nIn unpack_msg: \t%s' % msg.GetKey())
        time = float(int(msg.GetTime()*1000)/1000) # round to 3 decimals
        name = msg.GetKey() # 'z_____' String
        # sens = msg.GetSource() # 'g_____' String
        if msg.IsDouble():
            # var_type = 'double'
            valu = msg.GetDouble()
        elif msg.IsString():
            raise Exception('strings not supported')
        else:
            print('wtf? Unknown variable type')
        message = dict([['time',time],
                        ['name',name],
                        # ['type',var_type],
                        # ['sens',sens],
                        ['valu',valu]])
        pp(message)
        self.handle_msg(message)

    def handle_msg(self, msg):
        """ ==> primary function for directing msg info <== """
        print('\nIn handle_msg: \t%s' % msg['name'])
        if 'zpsrNumObs' in msg['name']:
            self.num_updated.emit(int(msg['valu']))
        else: # assume its a pos
            err = self.pack_err(msg)
            if err:
                self.err_updated.emit(err)
                print('MoosWidget :: error value shipped')
   
    def pack_err(self, msg):
        """gather message data and return it when packaged as error mag"""
        print('In pack_err')
        time = msg['time']
        name = msg['name']
        valu = msg['valu']

        hld = self.err_holder
        if time not in hld:
            hld[time] = {}
        hld[time][name] = valu
        if len(hld[time]) == 6:
            return ptolemy.ENError(\
                    hld[time]['zX'],    hld[time]['zY'],    hld[time]['zZ'],\
                    hld[time]['zpsrX'], hld[time]['zpsrY'], hld[time]['zpsrZ'])
        else: return False


################################################################################
if __name__ == '__main__':
    raise Exception('Do not run this file directly.')
