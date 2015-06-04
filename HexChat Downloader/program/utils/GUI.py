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
from Tkinter import IntVar
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Checkbutton

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
        
        #variables used by gui elements
        self.singlePackVar = StringVar()
        self.advancedGUI = IntVar()
        
        self.addButton("Single Pack Download", 10, 10, 200, 40, self.test)
        self.addTextBox(self.singlePackVar, 400, 10, 200, 40, self.test2)
        self.addCheckBox(self.advancedGUI, "Advanced Mode", 100, 400, 150, 40, self.test)
        
        #Start GUI
        self.gui.mainloop()
        
    """
    adds a button to the GUI
    @param text - the text to be displayed
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the button
    @param ySize - the height of the button
    @param command - the function to be invoked when this button is pressed
    """
    def addButton(self, text, xPos, yPos, xSize, ySize, command):
        button = Button(self.gui, command=command, text=text)
        button.pack()
        button.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a textBox to the gui, which saves its content to a predefined variable
    @param variable - the variable to be used and displayed
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the textBox
    @param ySize - the height of the textBox
    @param command - the function to be invoked when Enter is pressed
    """
    def addTextBox(self, variable, xPos, yPos, xSize, ySize, command):
        textBox = Entry(self.gui, textvariable=variable)
        textBox.pack()
        textBox.bind('<Return>', command)
        textBox.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a checkbox to the gui with the given parameters
    @param variable - the variable to be used
    @param text - the text to be displayed next to the checkbox
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the checkBox
    @param ySize - the height of the checkBox
    @param command - the function to be invoked when the checkBox is pressed
    """
    def addCheckBox(self, variable, text, xPos, yPos, xSize, ySize, command):
        checkBox = Checkbutton(self.gui, command=command, text=text, variable=variable)
        checkBox.pack()
        checkBox.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    def test(self):
        print self.advancedGUI.get()
    def test2(self, helpervar):
        print 2