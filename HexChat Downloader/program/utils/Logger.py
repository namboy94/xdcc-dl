"""
Logger
Class that handles all kinds of logging

Created on May 12, 2015
Modified on May 12, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports

"""
Logger
the class that handles logging
"""
class Logger(object):
    
    """
    Constructor
    Initializes a new Logger Object
    @param - scriptCreator - A previously initialized ScriptCreator object
    """
    def __init__(self,scriptCreator):
        self.scriptCreator = scriptCreator
        
    """
    printLogToConsole
    Prints a log to the console, containing all packs to be downloaded.
    """
    def printLogToConsole(self):
        print "LOG\n"
        for bot in self.scriptCreator.botList:
            if len(bot.packs) != 0:
                print "server: " + bot.serverName
                print "\tchannel: " + bot.channelName
                counter = 1
                for pack in bot.packs:
                    print "\t\tpack " + str(counter) + ": " + pack.packNumber
                    counter += 1