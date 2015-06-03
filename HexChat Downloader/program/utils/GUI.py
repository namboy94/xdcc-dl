"""
GUI
Class that implements a simple GUI

Created on May 31, 2015
Modified on June 1, 2015

@author Hermann Krumrey
@version 1.0
"""

#imports
from Tkinter import Tk
from Tkinter import StringVar
from Tkinter import Entry
from Tkinter import Button

"""
The Main GUI Class
"""
class DownloadGUI(object):

    """
    Constructor
    @param packFile - the file containing the packs
    @param serverFile - the file containing the server info
    @param scriptFile - the file which is used to control hexchat
    @param logger - object to log the projesses happening
    @param config - configuration object
    @param hexChatCommand - the command to invoke hexchat
    """
    def __init__(self,packFile, serverFile, scriptFile, scriptWriter, logger, config, hexChatCommand):
        self.packFile = packFile
        self.serverFile = serverFile
        self.scriptFile = scriptFile
        self.scriptWriter = scriptWriter
        self.logger = logger
        self.config = config
        self.hexChatCommand = hexChatCommand
        
    """
    starts the GUI
    """
    def guiStart(self):
        
        #Initialize GUI
        self.gui = Tk()
        self.gui.geometry("800x800+300+300")
        self.gui.title("HexChat Downloader GUI")
        self.gui.wm_resizable(False, False)
        
        #Start GUI
        self.gui.mainloop()
        
    """
    adds a button to the GUI
    @param text - the text to be displayed
    @param xPos - the x position in the window
    @param yPos - the y position in the windows
    @param xSize - the width of the button
    @param ySize - the height of the button
    @param function - the function to be invoked when this button is pressed
    """
    def addButton(self, text, xPos, yPos, xSize, ySize, function):
        button = Button(self.gui, width=xSize, height=ySize, command=function, text=text)
        button.pack()
        button.place(x=xPos, y=yPos)
        
    def test(self):
        print 1