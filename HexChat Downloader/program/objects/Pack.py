"""
Pack
Class that models a pack, complete with server and channel info

Created on May 6, 2015
Modified on May 9, 2015

@author Hermann Krumrey
@version 0.2
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