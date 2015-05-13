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
import email
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText

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
        
        msg = MIMEMultipart()
        
        msg['From'] = 'python@krumreyh.com'
        msg['To'] = 'hermann@krumreyh.com'
        msg['Subject'] = 'Python Test'
        
        textMessage = MIMEText("Hello, this is a friendly test.", 'plain')
        
        msg.attach(textMessage)
        
        smtp = smtplib.SMTP('smtp.strato.de', 25)
        smtp.set_debuglevel(1)
        smtp.starttls()
        smtp.login('python@krumreyh.com', 'KrUFcb@com3Y')
        
        
        smtp.sendmail(mailSender, mailReceiver, msg.as_string())
        smtp.quit()
        