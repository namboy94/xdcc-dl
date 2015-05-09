"""
ScriptCreator
Class that creates a hexchat python script, moves it into the hexchat auto load directory,
and finally executes hexchat

Created on May 9, 2015
Modified on May 9, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports


"""
ScriptCreator
the class that acts as bridge to Hexchat
"""
class ScriptCreator(object):
    
    """
    Constructor
    Initializes a new ScriptCreator object
    It combines a packList with a botList
    @param packList - list of packs to be downloaded
    @param botList - list of bots 
    """
    def __init__(self,packList,botList):
        
        self.botList = botList
        for pack in packList:
            added = False
            for bot in self.botList:
                if bot.botName == pack.botName:
                    bot.addPack(pack)
                    added = True
            if not added:
                print "Bot %s not found." % (pack.botName)
                    
    """
    packWriter
    """