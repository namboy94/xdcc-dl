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
Pack
Class that models a pack, complete with server and channel info

Created on May 6, 2015
Modified on May 9, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports

"""
Pack
The class that models a pack
"""
class Pack(object):
    
    """
    Constructor
    constructs a new Pack object
    @param botname - the name of the bot that holds this pack
    @param packNumber - the pack number
    """
    def __init__(self,botName,packNumber):
        self.botName = botName
        self.packNumber = packNumber