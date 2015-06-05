"""
GUI
Class that implements a simple GUI

Created on May 31, 2015

@author Hermann Krumrey
@version 1.5
"""

#imports
from Tkinter import Tk
from Tkinter import StringVar
from Tkinter import IntVar
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Label
from PIL import Image, ImageTk
import tkMessageBox
import platform
import os
from program.parsers.parserCollection import serverParse, packParse
from program.utils.ScriptCreator import ScriptCreator
from program.utils.Logger import Logger
from program.objects.Pack import Pack

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
        self.gui.geometry("450x100+300+300")
        self.gui.title("HexChat Downloader GUI")
        self.gui.wm_resizable(False, False)
        
        #variables used by gui elements
        self.singlePackVar = StringVar()
        self.advancedGUI = IntVar()
        self.emailLog = IntVar()
        
        #Initialize variables if needed
        self.emailLog.set(self.config.emailSwitch)
        
        #Add UI Elements (Simple Mode)
        self.addButton("Single Pack Download", 10, 10, 200, 40, self.downloadSinglePack)
        self.addTextBox(self.singlePackVar, 230, 10, 200, 40, self.downloadSinglePackOnEnter)
        self.addCheckBox(self.advancedGUI, "Advanced Mode", 50, 50, 150, 40, self.toggleAdvanced)
        self.addCheckBox(self.emailLog, "Send log Email?", 250, 50, 150, 40, self.toggleEmail)
        
        #Add UI Elements (Advanced Mode)
        self.addButton("Edit Packs", 10, 100, 200, 40, self.editPacks)
        self.addButton("Edit Servers", 230, 100, 200, 40, self.editServers)
        self.addButton("Start Batch Download", 125, 155, 200, 40, self.startBatchDownload)
        self.addButton("Switch to CLI", 320, 210, 100, 20, self.switchToCLI)
        self.addPicture("/home/hermann/Downloads/url.png", 100, 100, 100, 100)
        
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
        
    """
    adds a label to the GUI
    @param text - the text to be displayed by the label
    @param xPos - the x position in the window
    @param yPos - the y position in the window
    @param xSize - the width of the label
    @param ySize - the height of the label
    """
    def addLabel(self, text, xPos, yPos, xSize, ySize):
        label = Label(self.gui, text=text)
        label.pack()
        label.place(x=xPos, y=yPos, width=xSize, height=ySize)
        
    """
    adds a picture to the GUI
    @param file - the file containing the picture to be added
    @param xPos - the picture's x-position on the GUI
    @param yPos - the picture's y-position on the GUI
    @param xSize - the width of the picture
    @param ySize - the height of the picture
    """
    def addPicture(self, imageFile, xPos, yPos, xSize, ySize):
        image = Image.open(imageFile)
        clip = ImageTk.PhotoImage(image)
        picture = Label(image=clip)
        picture.image = image
        picture.pack()
        picture.place(x=xPos, y=yPos, width=xSize, height=ySize)
    
    """
    toggles advanced and simple UI mode
    """
    def toggleAdvanced(self):
        if self.advancedGUI.get() == 1:
            self.gui.geometry("450x250")
        else:
            self.gui.geometry("450x100")
            
    """
    toggles if an email log should be sent or not
    """
    def toggleEmail(self):
        lines = [line.rstrip('\n') for line in open(self.config.configFile)]
        configFile = open(self.config.configFile, "w")
        
        for line in lines:
            if line.startswith("email active = "):
                if self.config.emailSwitch:
                    configFile.write("email active = false\n")
                    self.config.emailSwitch = False
                else:
                    configFile.write("email active = true\n")
                    self.config.emailSwitch = True
            else:
                configFile.write(line + "\n")
        configFile.close()
            
    """
    Refreshes information from the data files
    """
    def refreshInformation(self):
        botList = []
        packList = []    
        serverParse(self.serverFile,botList)
        packParse(self.packFile,packList)
        self.scriptWriter = ScriptCreator(packList, botList, self.scriptFile, self.scriptWriter.hexChatLocation, self.hexChatCommand)
        self.logger = Logger(self.scriptWriter,self.logger.emailSender,self.logger.emailReceiver,self.logger.emailServer,self.logger.emailPort,self.logger.emailPass)
                
    """
    downloads a single pack based on the string entered in the textBox (on button press)
    """
    def downloadSinglePack(self):
        userInput = self.singlePackVar.get()
        if userInput.startswith("/msg ") and " xdcc send #" in userInput:   
            bot = userInput.split("/msg ")[1].split(" xdcc send #")[0]
            packno = userInput.split(" xdcc send #")[1]
            pack = Pack(bot, packno)
            tempPackList = [pack]
            tempBotList = []
            serverParse(self.serverFile, tempBotList)
            tempScriptWriter = ScriptCreator(tempPackList, tempBotList, self.scriptFile, self.scriptWriter.hexChatLocation, self.hexChatCommand)
            tempLogger = Logger(tempScriptWriter,self.logger.emailSender,self.logger.emailReceiver,self.logger.emailServer,self.logger.emailPort,self.logger.emailPass)
            tempScriptWriter.scriptExecuter()
            if self.config.emailSwitch: tempLogger.emailLog()
            tkMessageBox.showinfo("Download Complete", "Download of pack " + userInput + " completed")
        else:
            tkMessageBox.showerror("Error", "Incorrect Syntax")
    
    """
    downloads a single pack based on the string entered in the textBox (on enter)
    @param dummy - not used variable that's used to trick the system
    """
    def downloadSinglePackOnEnter(self, dummy):
        self.downloadSinglePack()
        
    """
    opens the server file with a text editor
    """
    def editServers(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.serverFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.serverFile + "\"")
        self.refreshInformation()
    
    """
    opens the pack file with a text editor
    """
    def editPacks(self):
        if platform.system() == "Linux":
            os.system(self.config.textEditor + " '" + self.packFile + "'")
        if platform.system() == "Windows":
            os.system("call \"" + self.config.textEditor + "\" \"" + self.packFile + "\"")
        self.refreshInformation()
        
    """
    starts a new batch download
    """
    def startBatchDownload(self):
        self.scriptWriter.scriptExecuter()
        if self.config.emailSwitch: self.logger.emailLog()
        tkMessageBox.showinfo("Batch Download Complete", "Download of all packs in packs.txt complete")
        
    """
    Switches the User Interface from GUI to CLI
    """
    def switchToCLI(self):
        lines = [line.rstrip('\n') for line in open(self.config.configFile)]
        configFile = open(self.config.configFile, "w")
        
        for line in lines:
            if line.startswith("gui on = "):
                self.config.guiSwitch = False
                configFile.write("gui on = false\n")
            else:
                configFile.write(line + "\n")
        configFile.close()
        self.gui.destroy()