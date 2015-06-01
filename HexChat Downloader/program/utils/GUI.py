"""
GUI
Class that implements a simple GUI

Created on May 31, 2015
Modified on June 1, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
import os
import platform
from Tkinter import Tk
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import IntVar
from Tkinter import Label
from Tkinter import Entry

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
        self.gui = Tk()
        self.gui.geometry("300x200+200+200")
        self.gui.title("HexChat Downloader GUI")
        
        #Add button for editing packs
        editPackButton = Button(self.gui, text="Edit Packs", width=30, command=self.editPacks)
        editPackButton.pack()
        
        #Add button for editing servers
        editPackButton = Button(self.gui, text="Edit Servers", width=30, command=self.editServers)
        editPackButton.pack()
        
        #Add button for starting the download
        editPackButton = Button(self.gui, text="Start Download", width=30, command=self.startDownload)
        editPackButton.pack()
        
        #Add Checkbox for email log
        self.emailLogVar = IntVar()
        emailLogCheckBox = Checkbutton(self.gui, text="Email Log", variable=self.emailLogVar, command=self.emailCheckBox)
        if self.config.emailSwitch: emailLogCheckBox.toggle()
        emailLogCheckBox.pack()
        
        #Add button to switch to CLI mode
        changeToCLIButton = Button(self.gui, text="Switch to Command Line Interface", width=30, command=self.changeToCLI)
        changeToCLIButton.pack()
    
        self.gui.mainloop()
        
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
        
    """
    emailCheckBox
    handles the checkbox for the email log
    """
    def emailCheckBox(self):
        lines = [line.rstrip('\n') for line in open(self.config.configFile)]
        configFile = open(self.config.configFile, "w")
        
        for line in lines:
            if line.startswith("email active = "):
                if self.config.emailSwitch:
                    configFile.write("email active = false\n")
                    self.config.emailSwitch = False
                else:
                    configFile.write("email active = true\n")
                    self.config.emailSwitch = True
            else:
                configFile.write(line + "\n")
        configFile.close()
        
    """
    changeToCLI
    changes the inerface to the userInputParser-powered CLI/Terminal/Command Line Interface
    """
    def changeToCLI(self):
        lines = [line.rstrip('\n') for line in open(self.config.configFile)]
        configFile = open(self.config.configFile, "w")
        
        for line in lines:
            if line.startswith("gui on = "):
                self.config.guiSwitch = False
                configFile.write("gui on = false\n")
            else:
                configFile.write(line + "\n")
        configFile.close()
        self.gui.destroy()