import ts3lib, ts3defines
from datetime import datetime
from ts3plugin import ts3plugin
from PythonQt.QtCore import QTimer


class onChannelJoin(ts3plugin):
    name = "Anti Channel Join"
    apiVersion = 21
    requestAutoload = False
    version = "1.0"
    author = "DatDraggy"
    description = "Kick clients that join your channel."
    offersConfigure = False
    commandKeyword = ""
    infoTitle = None
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Toggle Anti Channel Join", "")]
    hotkeys = []
    enabled = False
    debug = False
    channels = [9, 35, 36]
    uids = ["sKtX9Ig4aS2bhuM5F/qdZWCQeWA=", "i/uK7zbZa6nzVGRRDMsIL3XAxw0=", "09Hy4Je6E8aqB/ny+XYMDI144CY="]
    uidsMover = ["sKtX9Ig4aS2bhuM5F/qdZWCQeWA="]

    @staticmethod
    def timestamp(): return '[{:%Y-%m-%d %H:%M:%S}] '.format(datetime.now())

    def __init__(self):
        if self.debug: ts3lib.printMessageToCurrentTab("{0}[color=orange]{1}[/color] Plugin for pyTSon by [url=https://github.com/{2}]{2}[/url] loaded.".format(self.timestamp(), self.name, self.author))

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL and menuItemID == 0:
            self.enabled = not self.enabled
            ts3lib.printMessageToCurrentTab("{0}Set {1} to [color=yellow]{2}[/color]".format(self.timestamp(),self.name,self.enabled))

    def onClientMoveEvent(self, serverConnectionHandlerID, clientID, oldChannelID, newChannelID, visibility, moveMessage):
        (err, myid) = ts3lib.getClientID(serverConnectionHandlerID)
        if err != ts3defines.ERROR_ok:
            self.log(LogLevel.LogLevel_DEBUG,"error getting clientid : %s" % err)
            
        (err, myChannelID) = ts3lib.getChannelOfClient(serverConnectionHandlerID, myid)
        if self.debug:
            ts3lib.printMessageToCurrentTab("%s" % clientID)
            ts3lib.printMessageToCurrentTab("%s" % myid)
            ts3lib.printMessageToCurrentTab("%s" % newChannelID)
            ts3lib.printMessageToCurrentTab("%s" % myChannelID)
        if(newChannelID in self.channels or self.enabled and newChannelID == myChannelID and clientID != myid):
            if(self.debug):
                ts3lib.printMessageToCurrentTab("%s" % clientID)
                
            (err, clientUID) = ts3lib.getClientVariable(serverConnectionHandlerID, clientID, ts3defines.ClientProperties.CLIENT_UNIQUE_IDENTIFIER)
            
            if(self.debug):
                ts3lib.printMessageToCurrentTab("%s" % clientUID)
                
            if err != ts3defines.ERROR_ok:
                ts3lib.printMessageToCurrentTab("error getting uid: %s" % err)

            if(clientUID in self.uids):
                return 0
           
            err = ts3lib.requestClientMove(serverConnectionHandlerID, clientID, oldChannelID, "")
            if err != ts3defines.ERROR_ok:
                ts3lib.printMessageToCurrentTab("error moving: %s" % err)
              
    def onClientMoveMovedEvent(self, serverConnectionHandlerID, clientID, oldChannelID, newChannelID, visibility, moverID, moverName, moverUID, moveMessage):
        (err, myid) = ts3lib.getClientID(serverConnectionHandlerID)
        if err != ts3defines.ERROR_ok:
            self.log(LogLevel.LogLevel_DEBUG,"error getting clientid : %s" % err)
            
        (err, myChannelID) = ts3lib.getChannelOfClient(serverConnectionHandlerID, myid)
        if self.debug:
            ts3lib.printMessageToCurrentTab("%s" % clientID)
            ts3lib.printMessageToCurrentTab("%s" % myid)
            ts3lib.printMessageToCurrentTab("%s" % newChannelID)
            ts3lib.printMessageToCurrentTab("%s" % myChannelID)
            
        if(newChannelID in self.channels or self.enabled and newChannelID == myChannelID and clientID != myid and moverID != myid):
            ts3lib.printMessageToCurrentTab("%s" % clientID)
            (err, movedUID) = ts3lib.getClientVariable(serverConnectionHandlerID, clientID, ts3defines.ClientProperties.CLIENT_UNIQUE_IDENTIFIER)
            ts3lib.printMessageToCurrentTab("%s" % movedUID)
            if err != ts3defines.ERROR_ok:
                ts3lib.printMessageToCurrentTab("error getting uid: %s" % err)
            
            if((moverUID in self.uidsMover) or (movedUID in self.uids)):
                return 0
            
            err = ts3lib.requestClientMove(serverConnectionHandlerID, clientID, oldChannelID, "")
            if err != ts3defines.ERROR_ok:
                ts3lib.printMessageToCurrentTab("error moving: %s" % err)