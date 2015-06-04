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
            if self.userInput.lower() == "print": self.placeHolder()
            if self.userInput.lower() == "email log": self.placeHolder()
            if self.userInput.lower() == "start": self.placeHolder()
            if self.userInput.lower() == "switch": self.placeHolder()
            if self.userInput.lower() == "quit": self.placeHolder()
            
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

    def placeHolder(self):
        print 1
        self.validInput = True

"""
inputParser
parses user input and acts accordingly
@param packFile - the location of the packfile
@param serverFile - the location of the serverfile
@param scriptWriter - the scriptwriter loaded with the information of the pack- and server files.
def inputParser(packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
    
    running = True
    
    print "Welcome to the HexChat XDCC Downloader"
    userInput = raw_input("What would you like to do?\n")
    
    while running:
        
        validInput = False
        
        #downloads all packs from the packlist file
        if userInput == "start":
            running = False
            scriptWriter.scriptExecuter()
            if config.emailSwitch: logger.emailLog()
            break
        
        #quits the program
        if userInput == "quit":
            running = False
            break
        
        #allows to edit packs with a text editor
        if userInput == "edit packs":
            if platform.system() == "Linux":
                os.system(config.textEditor + " '" + packFile + "'")
            if platform.system() == "Windows":
                os.system("call \"" + config.textEditor + "\" \"" + packFile + "\"")
            validInput = True
            
        #allows to edit the server config with editor
        if userInput == "edit servers":
            if platform.system() == "Linux":
                os.system(config.textEditor + " '" + serverFile + "'")
            if platform.system() == "Windows":
                os.system("call \"" + config.textEditor + "\" \"" + serverFile + "\"")
            validInput = True
        
        #prints the parsed packs to the console    
        if userInput == "print":
            logger.printLogToConsole()
            validInput = True
            
        #sends an email to the user containing all packs to be downloaded
        if userInput == "email log":
            logger.emailLog()
            validInput = True
            

            
        #switches to GUI
        if userInput == "switch":
            lines = [line.rstrip('\n') for line in open(config.configFile)]
            configFile = open(config.configFile, "w")
            for line in lines:
                if line.startswith("gui on = "):
                    config.guiSwitch = True
                    configFile.write("gui on = true\n")
                else:
                    configFile.write(line + "\n")
            configFile.close()
            break
        
        #Input not understood
        if not validInput:
            print ("Input was not understood")
        
        #refresh information
        botList = []
        packList = []    
        serverParse(serverFile,botList)
        packParse(packFile,packList)
        scriptWriter = ScriptCreator(packList, botList, scriptFile, scriptWriter.hexChatLocation, hexChatCommand)
        logger = Logger(scriptWriter,logger.emailSender,logger.emailReceiver,logger.emailServer,logger.emailPort,logger.emailPass)
            
        #next prompt
        userInput = raw_input("What would you like to do?\n")
        """