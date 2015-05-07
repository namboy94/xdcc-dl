"""
Bot
Class that models a bot

Created on May 7, 2015
Modified on May 7, 2015

@author Hermann Krumrey
@version 0.1
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