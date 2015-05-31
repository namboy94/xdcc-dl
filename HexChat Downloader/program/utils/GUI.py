"""
GUI
Class that implements a simple GUI

Created on May 31, 2015
Modified on May 31, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
import sys
import os
import platform
from Tkinter import *

class DownloadGUI(object):

    def __init__(self, packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
        self.packFile = packFile
        self.serverFile = serverFile
        self.scriptFile = scriptFile
        self.scriptWriter = scriptWriter
        self.logger = logger
        self.config = config
        self.hexchatCommand = hexChatCommand
    
    """
    guiStart
    starts the graphical user interface
    """
    def guiStart(self):
        
        #Initialize GUI
        gui = Tk()
        gui.geometry("450x300+200+200")
        gui.title("HexChat Downloader GUI")
        
        #Add button for editing packs
        editPackButton = Button(gui, text="Edit Packs", width=20, command=self.editPacks)
        editPackButton.pack()
        
        #Add button for editing servers
        editPackButton = Button(gui, text="Edit Servers", width=20, command=self.editServers)
        editPackButton.pack()
        
        #Add button for starting the download
        editPackButton = Button(gui, text="Start Download", width=20, command=self.startDownload)
        editPackButton.pack()
    
        gui.mainloop()
        
    """
    editPacks
    starts a text editing program and edits a pack File
    """
    def editPacks(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.packFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.packFile + "\"")
            
    """
    editServers
    starts a tect editing program and edits a server file
    """
    def editServers(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.serverFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.serverFile + "\"")
            
    """
    startDownload
    starts a HexChat Download session based on the information in the local data files.
    """
    def startDownload(self):  
        self.scriptWriter.scriptExecuter()
        if self.config.emailSwitch: self.logger.emailLog()