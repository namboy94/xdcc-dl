"""
ScriptCreator
Class that creates a hexchat python script, moves it into the hexchat auto load directory,
and finally executes hexchat

Created on May 9, 2015
Modified on May 15, 2015

@author Hermann Krumrey
@version 1.1
"""

#imports
import os
import platform

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
    @param scriptFile - the location of the script file to be written to
    @param hexChatLocation - the location of the hexchat scripts.
    """
    def __init__(self,packList,botList,scriptFile,hexChatLocation):
        
        self.hexChatLocation = hexChatLocation
        self.scriptFileLocation = scriptFile
        self.botList = botList
        self.botPackMerger(packList)
        self.scriptInitializer(scriptFile)
        self.botPackWriter()
        self.scriptFinalizer()
        self.scriptFile.close()
                    
    """
    botPackMerger
    adds every pack in the packlist to the internal botlist
    @param packList - the packlist to be merged with the botlist
    """
    def botPackMerger(self,packList):
    
        for pack in packList:
            added = False
            for bot in self.botList:
                if bot.botName == pack.botName:
                    bot.addPack(pack)
                    added = True
            if not added:
                print "Bot %s not found." % (pack.botName)
        
    """
    scriptInitializer
    Initializes the scriptfile to be used with hexchat
    """
    def scriptInitializer(self,scriptFile):
        
        self.scriptFile = open(self.scriptFileLocation, "w")
        self.scriptFile.close()
        self.scriptFile = open(self.scriptFileLocation, "a")
        
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
    botPackWriter
    Writes the parsed content of the server and pack files to the script file
    """
    def botPackWriter(self):

        for bot in self.botList:
            for pack in bot.packs:
                channelString = "newserver irc://" + bot.serverName + "/" + bot.channelName
                packString = "msg " + bot.botName + " xdcc send #" + pack.packNumber
                
                self.scriptFile.write("channels.append(\"" + channelString + "\")\n")
                self.scriptFile.write("packs.append(\"" + packString + "\")\n")
            
        self.scriptFile.write("\n")
        
    """
    scriptFinalizer
    Finalizes the scriptfile to be used with hexchat
    """    
    def scriptFinalizer(self):
        
        self.scriptFile.write("hexchat.command(channels[0])\n")
        self.scriptFile.write("hexchat.hook_print(\"You Join\", download)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC STALL\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)\n")
        self.scriptFile.write("hexchat.hook_print(\"DCC Timeout\", downloadFailed)\n\n")
        
    """
    scriptExecutor
    Executes the script via HexChat's scripting API
    """
    def scriptExecuter(self):
        
        if platform.system() == "Linux":
            if not self.hexChatLocation.endswith("/"): self.hexChatLocation += "/"
            os.system("cp '" + self.scriptFileLocation + "' '" + self.hexChatLocation + "xdccScript.py'")
            os.system("hexchat")
            os.system("rm '" + self.hexChatLocation + "xdccScript.py'")
        
        if platform.system() == "Windows":
            print "Windows is not yet supported"
            #TODO
            os.system("xcopy \"" + self.scriptFileLocation + "\" \"" + self.hexChatLocation + "xdccScript.py\" /E /C /H /R /K /O /Y")
            os.system("hexchat location")
            os.system("del \"" + self.hexChatLocation + "xdccScript.py\"")