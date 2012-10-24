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
    numsat_updated = QtCore.Signal(int)
    err_updated = QtCore.Signal(float)

    def __init__(self, config, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.thread = MoosThread()
        self.desired_variables = config['desired_variables']
        
        self.moos_client = MOOSCommClient()
        self.moos_client.SetOnConnectCallBack(self.onConnect)
        self.moos_client.SetOnMailCallBack(self.onMail)
        self.moos_client.Run(self.thread.this_ip, self.thread.this_port, \
                             'lfviz', 50)
        # Check Connection
        for x in range(30):
            sleep(0.1)
            if self.moos_client.IsConnected():
                print("\nConnected to MOOSDB")
                break
        if not self.moos_client.IsConnected():
            print("MOOSCommClient Error:: Failed to Connect to MOOSDB")
            sys.exit(-1)

        self.fvel_holder = {}
        self.path_holder = {}

    ### Primary MOOS Functions ###
    def onConnect(self):
        """MOOS callback - required in every MOOS app's class definition"""
        print('In MoosWidget.onConnect :: waiting for mail..')
        for var in self.desired_variables:
            self.moos_client.Register(var)
        return

    def onMail(self):
        """MOOS callback - required in every MOOS app's class definition"""
        # print('\n--- In MoosWidget.onMail :: Retrieving inbox contents ---')
        for message in self.moos_client.FetchRecentMail():
            self.unpack_msg(message)
            pass
        return True

    ### Mail handling functions ###
    def unpack_msg(self, msg):
            """parse moos messages. put into dictionary
            handles conversion of any strings
            """
            # print('\nIn unpack_msg: \t%s' % msg.GetKey())
            time = float(int(msg.GetTime()*1000)/1000) # round to 3 decimals
            name = msg.GetKey() # 'z_____' String
            sens = msg.GetSource() # 'g_____' String
            if msg.IsDouble():
                var_type = 'double'
                valu = msg.GetDouble()
            elif msg.IsString():
                var_type = 'string'
                if (name == 'zRelPath_E') or (name == 'zRelPath_N'):
                    # valu = self.crumble_string_msg(msg.GetString())
                    pass
                else:
                    raise Exception('unknown string name')
            else:
                print('wtf? Unknown variable type')
            message = dict([['time',time],
                            ['name',name],
                            ['type',var_type],
                            ['sens',sens],
                            ['valu',valu]])
            # pp(message)
    #         self.handle_msg(message)

    # def crumble_string_msg(self, str_in):
    #     """Turns the relative path strings into float lists"""
    #     # pp(str_in)
    #     useless = str_in.split(']')[1][1:-2]
    #     # pp(useless)
    #     useless = useless.split(',')
    #     # pp(useless)
    #     path = []
    #     if useless == ['']: # Handle none path by setting to a default
    #         print('MOOS:: received empty path')
    #         useless = ['0','1']
    #     # pp(useless)
    #     for pt in useless:
    #         path.append(float(pt))
    #     return path

    # def handle_msg(self, msg):
    #     """ ==> primary function for directing msg info <== """
    #     # print('\nIn handle_msg: \t%s' % msg['name'])
    #     if 'zFoll_Vel_' in msg['name']:
    #         fvel = self.pack_fvel(msg)
    #         if fvel:
    #             self.fvel_updated.emit(fvel)
    #     elif 'zRelPath_' in msg['name']:
    #         path = self.pack_path(msg)
    #         if path:
    #             self.path_updated.emit(path)
    #     else:
    #         print('MoosWidget.handle_msg::Unhandled message:\t%s' % msg['name'])

    # ##### Functions that gather message data and return it when packaged properly ##
    # def pack_fvel(self, msg):
    #     """takes the follower velocity messages and turns into velocity vector
    #     """
    #     # print('In pack_fvel: \t%s = %s' % (msg['name'], msg['valu']))
    #     holder = self.fvel_holder
    #     time = msg['time']
    #     name = msg['name']
    #     valu = msg['valu']
        
    #     if time not in holder:
    #         holder[time] = {}
    #     holder[time][name] = valu
    #     if len(holder[time]) == 2:
    #         vel_e = holder[time]['zFoll_Vel_E']
    #         vel_n = holder[time]['zFoll_Vel_N']
    #         vel_mag = ptolemy.euclideanDist_2(0,0, vel_e,vel_n)
    #         vel = (vel_e, vel_n, vel_mag)
    #         return vel
    #     else:
    #         return False

    # def pack_path(self, msg):
    #     """takes rel path messages and turns into list of QPoint, 
    #     requires pulling from holder
    #     mw is the MainWindow instance
    #     msg is either a north or east path list
    #     returns false if just put in the first half of necessary data
    #     """
    #     # print('\nIn MoosWidget.pack_path: %s' % msg['name'])
    #     holder = self.path_holder
    #     time = msg['time']
    #     name = msg['name']
    #     valu = msg['valu']
        
    #     if time not in holder:
    #         holder[time] = {}
    #     holder[time][name] = valu
    #     if len(holder[time]) == 2: # set now completed - ship it
    #         # check lengths
    #         print('MoosWidget.pack_path :: Shipping...')
    #         n = len(holder[time]['zRelPath_N'])
    #         if len(holder[time]['zRelPath_E']) != n: # check lengths
    #             print('MoosWidget.pack_path :: Warning :: Path length mismatch')
    #         else:
    #             pts = []
    #             for pt in range(n): 
    #                 new_pt = (holder[time]['zRelPath_E'][pt], \
    #                           holder[time]['zRelPath_N'][pt])
    #                 pts.append(new_pt)
    #             # path = dict([['time', msg['time']], ['pts', pts]])
    #             return pts
    #     else:
    #         return False # tell handle_msg not to ship it off

################################################################################
if __name__ == '__main__':
    raise Exception('Do not run this file directly.')
