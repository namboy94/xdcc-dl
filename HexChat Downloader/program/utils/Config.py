"""
Config
Class that parses a config file and stores these values

Created on May 15, 2015
Modified on May 30, 2015

@author Hermann Krumrey
@version 1.2
"""

#imports
import sys
import re
import os
import platform

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
        
        self.configFile = configFile
        lines = [line.rstrip('\n') for line in open(configFile)]
        
        ConfigCompleteChecker = [False, False, False, False, False, False, False, False]
        
        for line in lines:
            if line.startswith("text editor = "):
                self.textEditor = line.split("text editor = ")[1]
                ConfigCompleteChecker[0] = True
                if len(self.textEditor) == 1: ConfigCompleteChecker[0] = False
                
        if not ConfigCompleteChecker[0]:
            print "No text editor set. Please set a text editor in the config file"
            sys.exit(1)
        
        for line in lines:
            if line.startswith("email sender = "):
                self.emailSender = line.split("email sender = ")[1]
                self.checkEmailAdress(self.emailSender)
                ConfigCompleteChecker[1] = True
            if line.startswith("email receiver = "):
                self.emailReceiver = line.split("email receiver = ")[1]
                self.checkEmailAdress(self.emailReceiver)
                ConfigCompleteChecker[2] = True
            if line.startswith("email password = "):
                self.emailPassword = line.split("email password = ")[1]
                ConfigCompleteChecker[3] = True
            if line.startswith("email server = "):
                self.emailServer = line.split("email server = ")[1]
                self.checkServer(self.emailServer)
                ConfigCompleteChecker[4] = True
            if line.startswith("email port = "):
                self.emailPort = int(line.split("email port = ")[1])
                self.checkPort(self.emailPort)
                ConfigCompleteChecker[5] = True
            if line.lower() == "email active = true": 
                self.emailSwitch = True
                ConfigCompleteChecker[6] = True
            if line == "email active = false":
                self.emailSwitch = False
                ConfigCompleteChecker[6] = True
            if line.lower() == "gui on = true":
                self.guiSwitch = True
                ConfigCompleteChecker[7] = True
            if line.lower() == "gui on = false":
                self.guiSwitch = False
                ConfigCompleteChecker[7] = True
        
        for check in ConfigCompleteChecker:
            if not check:
                print "Config File incomplete, please edit the config file."
                self.openConfigFile()
                self.configComplete = False
        self.configComplete = True
                
                
    """
    checkEmailAdress
    checks if an email adress is a valid email adress
    @param the email adress to be checked
    """
    def checkEmailAdress(self, email):
        
        emailRegex = re.compile("[^ ]+@[^ ]+.[^ ]+")
        if not emailRegex.match(email):
            print "Invalid email adress " + email
            self.openConfigFile()
            
    """
    checkPort
    checks if a valid smtp port was entered
    @param the port to be checked
    """
    def checkPort(self, port):
        
        try: port = int(port)
        except ValueError:
            print "Invalid SMTP port " + str(port)
            self.openConfigFile()
            
    """
    checkServer
    checks if a valid SMTP server was entered
    @param the server to be checked
    """
    def checkServer(self, server):
        
        serverRegex = re.compile("smtp.[^ ]+.[^ ]+")
        if not serverRegex.match(server):
            print "Invalid SMTP server " + server
            self.openConfigFile()
           
    """
    openConfigFile
    opens the config file for editing
    """ 
    def openConfigFile(self):
        if platform.system() == "Linux":
            os.system(self.textEditor + " '" + self.configFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.textEditor + "\" \"" + self.configFile + "\"")