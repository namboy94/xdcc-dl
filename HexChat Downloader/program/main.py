"""
main
The main part of the program that combines all the different submodules to form a working program.

Created on May 6, 2015
Modified on May 12, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
import sys
import platform
import getpass
from program.parsers.parserCollection import serverParse
from program.parsers.parserCollection import packParse
from program.parsers.parserCollection import inputParser
from program.utils.ScriptCreator import ScriptCreator

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
    scriptFile = upperDirectory + "/program/data/temp/script.py"

elif platform.system() == "Windows":
    print "Sorry, Windows is not supported yet"
    sys.exit(1)
else:
    print "Sorry, this operating system is not supported"
    sys.exit(1)

botList = []
serverParse(serverFile,botList)
packList = []
packParse(packFile,packList)
hexChatScriptDirectory = "/home/" + getpass.getuser() + "/.config/hexchat/addons"
scriptWriter = ScriptCreator(packList, botList, scriptFile, hexChatScriptDirectory)
inputParser(packFile, serverFile, scriptWriter)
