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
    def __init__(self,packList,botList,scriptFile):
        
        self.botList = botList
        for pack in packList:
            added = False
            for bot in self.botList:
                if bot.botName == pack.botName:
                    bot.addPack(pack)
                    added = True
            if not added:
                print "Bot %s not found." % (pack.botName)
        
        self.scriptInitializer(scriptFile)
        for bot in self.botList:
            self.botPackWriter(bot)
            
        self.scriptFile.close()
                    
    """
    botPackWriter
    """
    def botPackWriter(self,bot):
        
        for pack in bot.packs:
            self.scriptFile.write("def join_" + pack.botName + pack.packNumber + "(word, word_eol, userdata):\n")
            self.scriptFile.write("\t'hexchat.command(msg " + pack.botName + " xdcc send #" + pack.packnumber + "'\n")
            self.scriptFile.write("\treturn hexchat.EAT_HEXCHAT\n")
            self.scriptFile.write("hexchat.command('newserver irc://" + bot.serverName + "/" + bot.channelName + "')\n")
            self.scriptFile.write("hexchat.hook_print(\"You Join\", join_" + pack.botName + pack.packNumber + ")\n")
            self.scriptFile.write("hexchat.hook_print(\"DCC RECV Complete\", quitChannel\n\n")
        
        
    """
    scriptInitializer
    """
    def scriptInitializer(self,scriptFile):
        
        self.scriptFile = open(scriptFile, "a")
        self.scriptFile.write("__module_name__ = \"xdcc_executer\"\n")
        self.scriptFile.write("__module_version__ = \"0.1\"\n")
        self.scriptFile.write("__module_description__ = \"Python XDCC Executer\"\n\n")
        self.scriptFile.write("import hexchat\n\n")
        self.scriptFile.write("def quitChannel(word, word_eol, userdata):\n")
        self.scriptFile.write("\thexchat.command('quit')\n")
        self.scriptFile.write("\t return hexchat.EAT-HEXCHAT\n\n")
        
        