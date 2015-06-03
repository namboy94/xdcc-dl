"""
GUI
Class that implements a simple GUI

Created on May 31, 2015
Modified on June 1, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
from Tkinter import Tk

"""
The Main GUI Class
"""
class DownloadGUI(object):

    def __init__(self,packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
        self.packFile = packFile
        self.serverFile = serverFile
        self.scriptFile = scriptFile
        self.scriptWriter = scriptWriter
        self.logger = logger
        self.config = config
        self.hexChatCommand = hexChatCommand
        
    def guiStart(self):
        
        #Initialize GUI
        self.gui = Tk()
        self.gui.geometry("300x200+200+200")
        self.gui.title("HexChat Downloader GUI")
        self.gui.wm_resizable(False, False)
        
        #Start GUI
        self.gui.mainloop()