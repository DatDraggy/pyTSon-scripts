from ts3plugin import ts3plugin
from PythonQt.QtCore import QTimer, Qt
import ts3defines, ts3lib


class onStartup(ts3plugin):
    name = "Doublecocks onStartup"
    apiVersion = 21
    requestAutoload = True
    version = "1"
    author = "Kieran, Bluscream"
    description = ""
    menuItems = []
    hotkeys = []
    offersConfigure = False
    commandKeyword = ""
    infoTitle = None
    timers = {}
    debug = True
    setconnectioninfo = "~cmdsetconnectioninfo~sconnection_ping=1337~sconnection_ping_deviation=0~sconnection_packets_sent_speech=1~sconnection_packets_sent_keepalive=1~sconnection_packets_sent_control=1~sconnection_bytes_sent_speech=1~sconnection_bytes_sent_keepalive=1~sconnection_bytes_sent_control=1~sconnection_packets_received_speech=1~sconnection_packets_received_keepalive=1~sconnection_packets_received_control=1~sconnection_bytes_received_speech=1~sconnection_bytes_received_keepalive=1~sconnection_bytes_received_control=1~sconnection_server2client_packetloss_speech=0~sconnection_server2client_packetloss_keepalive=0~sconnection_server2client_packetloss_control=0~sconnection_server2client_packetloss_total=0~sconnection_bandwidth_sent_last_second_speech=1~sconnection_bandwidth_sent_last_second_keepalive=1~sconnection_bandwidth_sent_last_second_control=1~sconnection_bandwidth_sent_last_minute_speech=1~sconnection_bandwidth_sent_last_minute_keepalive=1~sconnection_bandwidth_sent_last_minute_control=1"
    badgeCommand = "~cmdclientupdate~sclient_badges=overwolf=0:badges=94ec66de-5940-4e38-b002-970df0cf6c94,c9e97536-5a2d-4c8e-a135-af404587a472,450f81c1-ab41-4211-a338-222fa94ed157"

    def __init__(self):        
        self.startTimer(ts3lib.getCurrentServerConnectionHandlerID())

    def stop(self):
        for schid, timer in self.timers.items():
            self.stopTimer(schid)

    def startTimer(self, schid):
        self.timers[schid] = QTimer()
        self.timers[schid].timeout.connect(self.tick)
        self.timers[schid].start(1000)

    def stopTimer(self, schid):
        if schid in self.timers:
            self.timers[schid].stop()
            del self.timers[schid]

    def onConnectStatusChangeEvent(self, schid, newStatus, errorNumber):
        if newStatus == ts3defines.ConnectStatus.STATUS_CONNECTING:
            pass
        elif newStatus == ts3defines.ConnectStatus.STATUS_CONNECTED:
            pass
        elif newStatus == ts3defines.ConnectStatus.STATUS_CONNECTION_ESTABLISHING:
            pass
        elif newStatus == ts3defines.ConnectStatus.STATUS_CONNECTION_ESTABLISHED:
            ts3lib.requestSendServerTextMsg(schid, self.badgeCommand)
        elif newStatus == ts3defines.ConnectStatus.STATUS_DISCONNECTED:
            self.stopTimer(schid)

    def tick(self):
        try:
            ts3lib.requestSendServerTextMsg(ts3lib.getCurrentServerConnectionHandlerID(), self.setconnectioninfo)
        except:
            print(format_exc())