"""
Config
Class that parses a config file and stores these values

Created on May 15, 2015
Modified on May 15, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
import sys

"""
Config
the class that parses and stores configs.
"""
class Config(object):
    
    """
    Constructor
    Initializes a new Config Object
    @param configFile - the configuration file to be parsed
    """
    def __init__(self,configFile):
        
        lines = [line.rstrip('\n') for line in open(configFile)]
        
        ConfigCompleteChecker = [False, False, False, False, False, False]
        
        for line in lines:
            if line.startswith("email sender = "):
                self.emailSender = line.split("email sender = ")[1]
                ConfigCompleteChecker[0] = True
            if line.startswith("email receiver = "):
                self.emailReceiver = line.split("email receiver = ")[1]
                ConfigCompleteChecker[1] = True
            if line.startswith("email password = "):
                self.emailPassword = line.split("email password = ")[1]
                ConfigCompleteChecker[2] = True
            if line.startswith("email server = "):
                self.emailServer = line.split("email server = ")[1]
                ConfigCompleteChecker[3] = True
            if line.startswith("email port = "):
                self.emailPort = int(line.split("email port = ")[1])
                ConfigCompleteChecker[4] = True
            if line.startswith("text editor = "):
                self.textEditor = line.split("text editor = ")[1]
                ConfigCompleteChecker[5] = True
        
        for check in ConfigCompleteChecker:
            if not check:
                print "Config File incomplete, please use a complete config file."
                sys.exit(1)