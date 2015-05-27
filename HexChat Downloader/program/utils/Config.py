"""
Config
Class that parses a config file and stores these values

Created on May 15, 2015
Modified on May 27, 2015

@author Hermann Krumrey
@version 1.1
"""

#imports
import sys
import re

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
        
        ConfigCompleteChecker = [False, False, False, False, False, False, False]
        
        for line in lines:
            if line.startswith("email sender = "):
                self.emailSender = line.split("email sender = ")[1]
                self.checkEmailAdress(self.emailSender)
                ConfigCompleteChecker[0] = True
            if line.startswith("email receiver = "):
                self.emailReceiver = line.split("email receiver = ")[1]
                self.checkEmailAdress(self.emailReceiver)
                ConfigCompleteChecker[1] = True
            if line.startswith("email password = "):
                self.emailPassword = line.split("email password = ")[1]
                ConfigCompleteChecker[2] = True
            if line.startswith("email server = "):
                self.emailServer = line.split("email server = ")[1]
                self.checkServer(self.emailServer)
                ConfigCompleteChecker[3] = True
            if line.startswith("email port = "):
                self.emailPort = int(line.split("email port = ")[1])
                self.checkPort(self.emailPort)
                ConfigCompleteChecker[4] = True
            if line.startswith("text editor = "):
                self.textEditor = line.split("text editor = ")[1]
                ConfigCompleteChecker[5] = True
            if line.lower() == "email active = true":
                self.emailSwitch = True
                ConfigCompleteChecker[6] = True
            if line == "email active = false":
                self.emailSwitch = False
                ConfigCompleteChecker[6] = True
        
        for check in ConfigCompleteChecker:
            if not check:
                print "Config File incomplete, please use a complete config file."
                sys.exit(1)
                
    """
    checkEmailAdress
    checks if an email adress is a valid email adress
    @param the email adress to be checked
    """
    def checkEmailAdress(self, email):
        
        emailRegex = re.compile("[^ ]+@[^ ]+.[^ ]+")
        if not emailRegex.match(email):
            print "Invalid email adress " + email
            sys.exit(1)
            
    """
    checkPort
    checks if a valid smtp port was entered
    @param the port to be checked
    """
    def checkPort(self, port):
        
        try: port = int(port)
        except ValueError:
            print "Invalid SMTP port " + str(port)
            sys.exit(1)
            
    """
    checkServer
    checks if a valid SMTP server was entered
    @param the server to be checked
    """
    def checkServer(self, server):
        
        serverRegex = re.compile("smtp.[^ ]+.[^ ]+")
        if not serverRegex.match(server):
            print "Invalid SMTP server " + server
            sys.exit(1)