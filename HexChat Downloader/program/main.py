"""
main
The main part of the program that combines all the different submodules to form a working program.

Created on May 6, 2015

@author Hermann Krumrey
@version 1.5
"""

#imports
import sys
import platform
import getpass
import os

#OS check and setup
if platform.system() == "Linux":
    #fix pythonpath
    splitPath = sys.argv[0].split("/")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    #set inputFiles
    serverFile = upperDirectory + "/program/data/servers.config"
    packFile = upperDirectory + "/program/data/packs.txt"
    configFile = upperDirectory + "/program/data/config.ini"
    scriptFile = upperDirectory + "/program/data/temp/script.py"
    hexChatScriptDirectory = "/home/" + getpass.getuser() + "/.config/hexchat/addons/"
    hexChatCommand = "hexchat"
elif platform.system() == "Windows":
    #fix pythonpath
    splitPath = sys.argv[0].split("\\")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    #set inputFiles
    serverFile = upperDirectory + "\\program\\data\\servers.config"
    packFile = upperDirectory + "\\program\\data\\packs.txt"
    configFile = upperDirectory + "\\program\\data\\config.ini"
    scriptFile = upperDirectory + "\\program\\data\\temp\\script.py"
    hexChatScriptDirectory = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\HexChat\\addons\\"
    hexChatCommand = upperDirectory + "\\program\\resources\\HexChat 2.10.2 (x64) Portable\\HexChat\\hexchat.exe"
    
    if not os.path.isdir(hexChatScriptDirectory):
        os.system("\"" + hexChatCommand + "\"")
else:
    print "Sorry, this operating system is not supported"
    sys.exit(1)
    
#Secondary Imports (Needed Pythonpath fix)
from program.parsers.parserCollection import serverParse
from program.parsers.parserCollection import packParse
from program.parsers.CLI import CLI
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
from program.utils.Config import Config
from program.utils.GUI import DownloadGUI

config = Config(configFile)
while not config.configComplete:
    config = Config(configFile)

#Variable Declarations
botList = []
packList = []

#Execution
serverParse(serverFile,botList)
packParse(packFile,packList)
scriptWriter = ScriptCreator(packList, botList, scriptFile, hexChatScriptDirectory, hexChatCommand)
logger = Logger(scriptWriter, config.emailSender, config.emailReceiver, config.emailServer, config.emailPort, config.emailPassword)

#Starts user interface
while True:
    if config.guiSwitch:
        gui = DownloadGUI(packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand)
        gui.guiStart()
        if config.guiSwitch:
            break
    else:
        cli = CLI(packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand)
        cli.mainLoop()
        if not config.guiSwitch:
            break