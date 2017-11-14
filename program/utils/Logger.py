"""
Copyright 2015-2017 Hermann Krumrey

This file is part of hexchat-downloader.

hexchat-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

hexchat-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with hexchat-downloader.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Logger
Class that handles all kinds of logging

Created on May 12, 2015

@author Hermann Krumrey
@version 1.5
"""

#imports
import smtplib
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
    @param scriptCreator - A previously initialized ScriptCreator object
    @param emailSender - The sender of the email, or the program's email adress.
    @param emailReceiver - The receiver of the log emails
    @param emailServer - the smtp server to be connected to
    @param emailPort - the port of the smtp server
    @param emailPass - the program's password on the smtp server
    """
    def __init__(self,scriptCreator,emailSender,emailReceiver,emailServer,emailPort,emailPass):
        self.scriptCreator = scriptCreator
        self.emailSender = emailSender
        self.emailReceiver = emailReceiver
        self.emailServer = emailServer
        self.emailPort = emailPort
        self.emailPass = emailPass
        
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
                print "\t\tbot: " + bot.botName
                counter = 1
                for pack in bot.packs:
                    print "\t\t\tpack " + str(counter) + ": " + pack.packNumber
                    counter += 1
    
    def emailLog(self):
        
        #initialize the email with headers
        msg = MIMEMultipart()
        msg['From'] = self.emailSender
        msg['To'] = self.emailReceiver
        msg['Subject'] = 'HexChat Downloader Log'
        
        #Write the body of the email.
        textMessage = MIMEText("HexChat Download Log\n\n", 'plain')
        msg.attach(textMessage)
        
        sortedBots = self.scriptCreator.botList
        sortedBots.sort(key=lambda x: x.channelName)
        sortedBots.sort(key=lambda x: x.serverName)
        previousChannel = ""
        previousServer = ""
        text = ""
        index = 0
        
        for bot in sortedBots:
            if len(bot.packs) != 0:
                if previousServer != bot.serverName:
                    text = "server: " + bot.serverName + "\n"
                if previousChannel != bot.channelName:
                    text += "\tchannel: " + bot.channelName + "\n"
                text += "\t\tbot: " + bot.botName + "\n"
                counter = 1
                for pack in bot.packs:
                    text += "\t\t\tpack " + str(counter) + ": " + pack.packNumber+ "\n"
                    counter += 1
                if index + 1 == len(sortedBots) or sortedBots[index + 1] != bot.serverName:        
                    msg.attach(MIMEText(text, 'plain'))
                    text = ""
                previousChannel = bot.channelName
                previousServer = bot.serverName
                index += 0
                   
        #Initialize Connection 
        smtp = smtplib.SMTP(self.emailServer, self.emailPort)
        smtp.set_debuglevel(1)
        smtp.starttls()
        smtp.login(self.emailSender, self.emailPass)
        
        #Send Email
        smtp.sendmail(self.emailSender, self.emailReceiver, msg.as_string())
        smtp.quit()
        