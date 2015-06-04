"""
parserCollection
collection of methods that parse files.

Created on May 9, 2015

@author Hermann Krumrey
@version 1.5
"""

#imports
from program.objects.Bot import Bot
from program.objects.Pack import Pack
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
import os
import platform

"""
serverParse
method that parses a server file, saves the information to Bot objects
and appends them to a list.
@param serverFile - the server file to be parsed
@param botList - list of bots to be used
"""
def serverParse(serverFile, botList):
    
    #Saves all lines in the file to a list
    lines = [line.rstrip('\n') for line in open(serverFile)]
    
    for line in lines:
        if not "#" in line and line != "":
            botName = line.split(" @ ")[0]
            serverChannel = line.split(" @ ")[1]
            serverName = serverChannel.split("/")[0]
            channelName = serverChannel.split("/")[1]
            bot = Bot(botName,serverName,channelName)
            botList.append(bot)
            
"""
packParse
method that parses a pack file, svaes the data to Pack objects and
appends them to a list
@param packFile - the pack file to be parsed
@param packList - the list of packs to which the packs should be appended to.
"""
def packParse(packFile, packList):
    
    #Saves all lines in the file to a list
    lines = [line.rstrip('\n') for line in open(packFile)]
    
    #variables for better input parsing
    episodeHopper = 0
    hopping = False
    
    for line in lines:
        if not "###" in line and line != "":
            if "..." in line:
                hopping = True
                episodeHopper = int(line.split("...")[1])
                previousPack = packList[len(packList) - 1]
            elif hopping:
                hopping = False
                splitAtXdccSend = line.split(" xdcc send #")
                botName = splitAtXdccSend[0].split("/msg ")[1]
                episodeHop = int(previousPack.packNumber) + episodeHopper
                while episodeHop <= int(splitAtXdccSend[1]):
                    pack = Pack(botName, str(episodeHop))
                    packList.append(pack)
                    episodeHop += episodeHopper
            else:
                splitAtXdccSend = line.split(" xdcc send #")
                packNumber = splitAtXdccSend[1]
                botName = splitAtXdccSend[0].split("/msg ")[1]
                pack = Pack(botName,packNumber)
                packList.append(pack)
            
            
"""
inputParser
parses user input and acts accordingly
@param packFile - the location of the packfile
@param serverFile - the location of the serverfile
@param scriptWriter - the scriptwriter loaded with the information of the pack- and server files.
"""
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
            
        #downloads a single pack
        if userInput.startswith("/msg ") and " xdcc send #" in userInput:
            bot = userInput.split("/msg ")[1].split(" xdcc send #")[0]
            packno = userInput.split(" xdcc send #")[1]
            pack = Pack(bot, packno)
            tempPackList = [pack]
            tempBotList = []
            serverParse(serverFile, tempBotList)
            tempScriptWriter = ScriptCreator(tempPackList, tempBotList, scriptFile, scriptWriter.hexChatLocation, hexChatCommand)
            tempLogger = Logger(tempScriptWriter,logger.emailSender,logger.emailReceiver,logger.emailServer,logger.emailPort,logger.emailPass)
            tempScriptWriter.scriptExecuter()
            if config.emailSwitch: tempLogger.emailLog()
            print "Downloaded Single Pack " + userInput
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