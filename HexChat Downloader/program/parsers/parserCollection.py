"""
parserCollection
collection of methods that parse files.
Created on May 9, 2015
Modified on May 9, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
from program.objects.Bot import Bot
from program.objects.Pack import Pack

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
        if not "#" in line:
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
    
    for line in lines:
        if not "###" in line:
            splitAtXdccSend = line.split(" xdcc send #")
            packNumber = splitAtXdccSend[1]
            botName = splitAtXdccSend[0].split("/msg ")[1]
            pack = Pack(botName,packNumber)
            packList.append(pack)