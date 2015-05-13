"""
Logger
Class that handles all kinds of logging

Created on May 12, 2015
Modified on May 12, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
import smtplib
from aptdaemon.config import log
from twisted.spread.ui.gtk2util import login

"""
Logger
the class that handles logging
"""
class Logger(object):
    
    """
    Constructor
    Initializes a new Logger Object
    @param - scriptCreator - A previously initialized ScriptCreator object
    """
    def __init__(self,scriptCreator):
        self.scriptCreator = scriptCreator
        
    """
    printLogToConsole
    Prints a log to the console, containing all packs to be downloaded.
    """
    def printLogToConsole(self):
        print "LOG\n"
        for bot in self.scriptCreator.botList:
            if len(bot.packs) != 0:
                print "server: " + bot.serverName
                print "\tchannel: " + bot.channelName
                counter = 1
                for pack in bot.packs:
                    print "\t\tpack " + str(counter) + ": " + pack.packNumber
                    counter += 1
    
    def emailLog(self):
        mailSender = "python@krumreyh.com"
        mailReceiver = "hermann@krumreyh.com"
        
        smtpMessage = """From: Python <python@krumreyh.com>
        To: Hermann Krumrey <hermann@krumreyh.com>
        Subject: Python log
        
        This is the python's log'
        """
        
        smtp = smtplib.SMTP('smtp.strato.de', 25)
        smtp.set_debuglevel(1)
        #smtp.ehlo()
        smtp.starttls()
        smtp.login('python@krumreyh.com', 'KrUFcb@com3Y')
        
        
        smtp.sendmail(mailSender, mailReceiver, smtpMessage)
        smtp.quit()
        