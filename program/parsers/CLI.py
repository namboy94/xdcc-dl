"""
Copyright 2015-2017 Hermann Krumrey

This file is part of hexchat-downloader.

hexchat-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

hexchat-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with hexchat-downloader.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
CLI User Interface

Created on Jun 4, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
import platform
import os
from program.parsers.parserCollection import serverParse, packParse
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
from program.objects.Pack import Pack

"""
The CLI Parser object
"""
class CLI(object):
    
    """
    Constructor of the CLI object
    """
    def __init__(self, packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
        self.packFile = packFile
        self.serverFile = serverFile
        self.scriptFile = scriptFile
        self.scriptWriter = scriptWriter
        self.logger = logger
        self.config = config
        self.hexChatCommand = hexChatCommand
        
    """
    Starts the CLI.
    """
    def mainLoop(self):
        self.running = True
        
        while self.running:
            
            self.userInput = raw_input("What would you like to do?\n")
            self.validInput = False
            
            if self.userInput.lower() == "help": self.showHelp()
            if self.userInput.startswith("/msg ") and " xdcc send #" in self.userInput: self.downloadSinglePack()
            if self.userInput.lower() == "edit packs": self.editPacks()
            if self.userInput.lower() == "edit servers": self.editServers()
            if self.userInput.lower() == "print": self.printLog()
            if self.userInput.lower() == "email log": self.emailLog()
            if self.userInput.lower() == "start": self.startBatchDownload()
            if self.userInput.lower() == "switch": self.switchToGUI()
            if self.userInput.lower() == "quit": self.quit()
            
            if not self.validInput:
                print "Input was not understood. Enter help for a list of valid commands"
            
    """
    prints all currently available commands to the console
    """
    def showHelp(self):
        print "List of commands:\n"
        print "help                                                lists all available commands"
        print "print                                               prints all currently loaded packs from the packfile"
        print "email log                                           sends an email with all currently loaded packs from the packfile"
        print "edit packs                                          opens the packfile with a text editor"
        print "edit servers                                        opens the server list with a text editor"
        print "start                                               starts a batch download of all packs in the packfile"
        print "/msg <botname> xdcc send #<packnumber>              starts a download of a single pack"
        print "switch                                              switches to a GUI interface"
        print "quit                                                closes the program\n"
        self.validInput = True
    
    """
    Downloads a single pack
    """
    def downloadSinglePack(self): 
        bot = self.userInput.split("/msg ")[1].split(" xdcc send #")[0]
        packno = self.userInput.split(" xdcc send #")[1]
        pack = Pack(bot, packno)
        tempPackList = [pack]
        tempBotList = []
        serverParse(self.serverFile, tempBotList)
        tempScriptWriter = ScriptCreator(tempPackList, tempBotList, self.scriptFile, self.scriptWriter.hexChatLocation, self.hexChatCommand)
        tempLogger = Logger(tempScriptWriter,self.logger.emailSender,self.logger.emailReceiver,self.logger.emailServer,self.logger.emailPort,self.logger.emailPass)
        tempScriptWriter.scriptExecuter()
        if self.config.emailSwitch: tempLogger.emailLog()
        print "Download of pack " + self.userInput + " completed\n"
        self.validInput = True
        
    """
    Opens the pack file with a text editor
    """
    def editPacks(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.packFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.packFile + "\"")
        self.refreshInformation()
        self.validInput = True
        
    """
    Opens the server file with a text editor
    """
    def editServers(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.serverFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.serverFile + "\"")
        self.refreshInformation()
        self.validInput = True

    """
    Refreshes information from the data files
    """
    def refreshInformation(self):
        botList = []
        packList = []    
        serverParse(self.serverFile,botList)
        packParse(self.packFile,packList)
        self.scriptWriter = ScriptCreator(packList, botList, self.scriptFile, self.scriptWriter.hexChatLocation, self.hexChatCommand)
        self.logger = Logger(self.scriptWriter,self.logger.emailSender,self.logger.emailReceiver,self.logger.emailServer,self.logger.emailPort,self.logger.emailPass)

    """
    Prints a log to the console
    """
    def printLog(self):
        self.logger.printLogToConsole()
        self.validInput = True
        
    """
    Emails a log to the user's email adress
    """
    def emailLog(self):
        self.logger.emailLog()
        self.validInput = True

    """
    Starts a batch download of all packs in the packfile
    """
    def startBatchDownload(self):
        self.scriptWriter.scriptExecuter()
        if self.config.emailSwitch: self.logger.emailLog()
        print "Download of all packs in packs.txt complete\n"
        self.validInput = True

    """
    Switches to the GUI Interface
    """
    def switchToGUI(self):
        lines = [line.rstrip('\n') for line in open(self.config.configFile)]
        self.configFile = open(self.config.configFile, "w")
        for line in lines:
            if line.startswith("gui on = "):
                self.config.guiSwitch = True
                self.configFile.write("gui on = true\n")
            else:
                self.configFile.write(line + "\n")
        self.configFile.close()
        self.quit()
        self.validInput = True

    """
    Quits the program
    """
    def quit(self):
        self.running = False
        self.validInput = True