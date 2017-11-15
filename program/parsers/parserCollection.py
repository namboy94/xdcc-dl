"""
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

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
parserCollection
collection of methods that parse files.

Created on May 9, 2015

@author Hermann Krumrey
@version 1.5
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