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
Bot
Class that models a bot

Created on May 7, 2015
Modified on May 7, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports

"""
Bot
The class that models a bot
"""
class Bot(object):
    
    """
    Constructor
    constructs a new Bot object
    @param botName - the bot's name
    @param serverName - the server's name on which the bot is reacheable
    @param channelName - the channel's name on which the bot is reacheable
    """
    def __init__(self,botName,serverName,channelName):
        self.botName = botName
        self.serverName = serverName
        self.channelName = channelName
        self.packs = []
        
    """
    addPack
    adds a new pack to the internal packList
    @param pack - the pack to be added
    """
    def addPack(self,pack):
        self.packs.append(pack)