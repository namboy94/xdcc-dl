"""
main
The main part of the program that combines all the different submodules to form a working program.

Created on May 6, 2015
Modified on May 7, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
import sys
import platform
from program.parsers.serverParser import serverParse

#OS check and setup
if platform.system() == "Linux":
    #fix pythonpath
    splitPath = sys.argv[0].split("/")
    lengthToCut = len(splitPath[len(splitPath) - 1]) + len(splitPath[len(splitPath) - 2]) + 2
    upperDirectory = sys.argv[0][:-lengthToCut]
    sys.path.append(upperDirectory)
    
    #set serverFile
    serverFile = upperDirectory + "/program/data/servers.config"

elif platform.system() == "Windows":
    print "Sorry, Windows is not supported yet"
    sys.exit(1)
else:
    print "Sorry, this operating system is not supported"
    sys.exit(1)

botList = []
serverParse(serverFile,botList)

#TODOS

# Server File Parser (Complete)
# PacklistParser
# ScriptCreator
# ScriptMover
# HexStarter