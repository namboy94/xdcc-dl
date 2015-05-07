"""
main
The main part of the program that combines all the different submodules to form a working program.

Created on May 6, 2015
Modified on May 7, 2015

@author Hermann Krumrey
@version 0.1
"""
from program.parsers.serverParser import serverParse

#TODOS

# Server File Parser (Complete)
# PacklistParser
# ScriptCreator
# ScriptMover
# HexStarter

serverFile = ""
botList = []
serverParse(serverFile,botList)