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
from Tkinter import StringVar
from Tkinter import Entry
from program.objects.Pack import Pack
from program.parsers.parserCollection import serverParse
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
import tkMessageBox

class DownloadGUI(object):

    def __init__(self, packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
        self.packFile = packFile
        self.serverFile = serverFile
        self.scriptFile = scriptFile
        self.scriptWriter = scriptWriter
        self.logger = logger
        self.config = config
        self.hexChatCommand = hexChatCommand
    
    """
    guiStart
    starts the graphical user interface
    """
    def guiStart(self):
        
        #Initialize GUI
        self.gui = Tk()
        self.gui.geometry("300x100+200+200")
        self.gui.title("HexChat Downloader GUI")
        
        #Simple Single Download Interface
        self.singlePackVar = StringVar()
        singlePackEntry = Entry(self.gui, textvariable=self.singlePackVar)
        singlePackEntry.pack()
        startSingleDowloadButton = Button(self.gui, text="Start single pack download", width=30, command=self.singlePack)
        startSingleDowloadButton.pack()
        
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
        
        #Advanced Options Checkbox
        self.advancedVar = IntVar()
        self.advancedCheckBox = Checkbutton(self.gui, text="Advanced Mode", variable=self.advancedVar, command=self.advancedGUIStart)
        self.advancedCheckBox.pack()
    
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
    changes the interface to the userInputParser-powered CLI/Terminal/Command Line Interface
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
        
    """
    singlePack
    downloads a single XDCC pack
    """
    def singlePack(self):
        userInput = self.singlePackVar.get()
        if userInput.startswith("/msg ") and " xdcc send #" in userInput:   
            bot = userInput.split("/msg ")[1].split(" xdcc send #")[0]
            packno = userInput.split(" xdcc send #")[1]
            pack = Pack(bot, packno)
            tempPackList = [pack]
            tempBotList = []
            serverParse(self.serverFile, tempBotList)
            tempScriptWriter = ScriptCreator(tempPackList, tempBotList, self.scriptFile, self.scriptWriter.hexChatLocation, self.hexChatCommand)
            tempLogger = Logger(tempScriptWriter,self.logger.emailSender,self.logger.emailReceiver,self.logger.emailServer,self.logger.emailPort,self.logger.emailPass)
            tempScriptWriter.scriptExecuter()
            if self.config.emailSwitch: tempLogger.emailLog()
            tkMessageBox.showinfo("Download Complete", "Download of pack " + userInput + " completed")
        else:
            tkMessageBox.showerror("Error", "Incorrect Syntax")
            
    """
    advancedGUIStart
    starts the advanced GUI
    """
    def advancedGUIStart(self):
        if self.advancedVar.get() == 1:
            self.gui.geometry("300x200+200+200")
            
            #Add button for editing packs
            editPackButton = Button(self.gui, text="Edit Packs", width=30, command=self.editPacks)
            editPackButton.pack()
            
            #Add button for editing servers
            editPackButton = Button(self.gui, text="Edit Servers", width=30, command=self.editServers)
            editPackButton.pack()
            
        else:
            self.gui.removeAll()