"""
parserCollection
collection of methods that parse files.
Created on May 9, 2015
Modified on May 12, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
from program.objects.Bot import Bot
from program.objects.Pack import Pack
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
import os

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
def inputParser(packFile, serverFile, scriptFile, scriptWriter, logger):
    
    running = True
    
    print "Welcome to the HexChat XDCC Downloader"
    userInput = raw_input("What would you like to do?\n")
    
    while running:
        
        if userInput == "start":
            running = False
            scriptWriter.scriptExecuter()
            logger.emailLog()
            break
        elif userInput == "quit":
            running = False
            break
        elif userInput == "edit packs":
            os.system("gedit '" + packFile + "'")
        elif userInput == "edit servers":
            os.system("gedit '" + serverFile + "'")
        elif userInput == "print":
            logger.printLogToConsole()
        elif userInput == "email log":
            logger.emailLog()
        elif userInput.startswith("/msg ") and " xdcc send #" in userInput:
            bot = userInput.split("/msg ")[1].split(" xdcc send #")[0]
            packno = userInput.split(" xdcc send #")[1]
            pack = Pack(bot, packno)
            tempPackList = [pack]
            tempBotList = []
            serverParse(serverFile, tempBotList)
            tempScriptWriter = ScriptCreator(tempPackList, tempBotList, scriptFile, scriptWriter.hexChatLocation)
            tempLogger = Logger(tempScriptWriter,logger.emailSender,logger.emailReceiver,logger.emailServer,logger.emailPort,logger.emailPass)
            #tempScriptWriter.scriptExecuter()
            tempLogger.emailLog()
            print "Downloaded Single Pack " + userInput
        else:
            print ("Input was not understood")
        
        #refresh information
        botList = []
        packList = []    
        serverParse(serverFile,botList)
        packParse(packFile,packList)
        scriptWriter = ScriptCreator(packList, botList, scriptFile, scriptWriter.hexChatLocation)
        logger = Logger(scriptWriter,logger.emailSender,logger.emailReceiver,logger.emailServer,logger.emailPort,logger.emailPass)
            
        userInput = raw_input("What would you like to do?\n")