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
        self.scriptFinalizer()
            
        self.scriptFile.close()
                    
    """
    botPackWriter
    """
    def botPackWriter(self,bot):

        for pack in bot.packs:
            channelString = "newserver irc://" + bot.serverName + "/" + bot.channelName
            packString = "msg " + bot.botName + " xdcc send #" + pack.packNumber
            
            self.scriptFile.write("channels.append(\"" + channelString + "\")\n")
            self.scriptFile.write("packs.append(\"" + packString + "\")\n")
            
        self.scriptFile.write("\n")
        
    """
    scriptInitializer
    """
    def scriptInitializer(self,scriptFile):
        
        self.scriptFile = open(scriptFile, "a")
        self.scriptFile.write("__module_name__ = \"xdcc_executer\"\n")
        self.scriptFile.write("__module_version__ = \"0.1\"\n")
        self.scriptFile.write("__module_description__ = \"Python XDCC Executer\"\n\n")
        
        self.scriptFile.write("import hexchat\n")
        self.scriptFile.write("import sys\n\n")
        
        self.scriptFile.write("def download(word, word_eol, userdata):\n")
        self.scriptFile.write("\thexchat.command(packs[0])\n")
        self.scriptFile.write("\treturn hexchat.EAT_HEXCHAT\n\n")
        
        self.scriptFile.write("def downloadComplete(word, word_eol, userdata):\n")
        self.scriptFile.write("\thexchat.command('quit')\n")
        self.scriptFile.write("\tchannels.pop(0)\n")
        self.scriptFile.write("\tpacks.pop(0)\n")
        self.scriptFile.write("\tif len(channels) == 0:\n")
        self.scriptFile.write("\t\tprint \"DOWNLOADS COMPLETE\"\n")
        self.scriptFile.write("\t\tsys.exit(1)\n")
        self.scriptFile.write("\telse:\n")
        self.scriptFile.write("\t\thexchat.command(channels[0])\n")
        self.scriptFile.write("\treturn hexchat.EAT_HEXCHAT\n\n")
        
        self.scriptFile.write("def downloadFailed(word, word_eol, userdata):\n")
        self.scriptFile.write("\tfailed.append(packs[0])\n")
        self.scriptFile.write("\thexchat.command('quit')\n")
        self.scriptFile.write("\tchannels.pop(0)\n")
        self.scriptFile.write("\tpacks.pop(0)\n")
        self.scriptFile.write("\tif len(channels) == 0:\n")
        self.scriptFile.write("\t\tprint \"DOWNLOADS COMPLETE\"\n")
        self.scriptFile.write("\t\tsys.exit(1)\n")
        self.scriptFile.write("\telse:\n")
        self.scriptFile.write("\t\thexchat.command(channels[0])\n")
        self.scriptFile.write("\treturn hexchat.EAT_HEXCHAT\n\n")
        
        self.scriptFile.write("failed = []\n")
        self.scriptFile.write("channels = []\n")
        self.scriptFile.write("packs = []\n\n")
        
    """
    scriptFinalizer
    """    
    def scriptFinalizer(self):
        
        self.scriptFile.write("hexchat.command(channels[0])\n")
        self.scriptFile.write("hexchat.hook_print(\"You Join\", download)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC STALL\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC Timeout\", downloadFailed)\n\n")