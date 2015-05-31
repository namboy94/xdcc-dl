"""
GUI
outsourced method that implements a simple GUI

Created on May 31, 2015
Modified on May 31, 2015

@author Hermann Krumrey
@version 0.1
"""

#imports
import sys
from Tkinter import *

"""
guiStart
starts the graphical user interface
"""
def guiStart():
    
    gui = Tk()
    gui.geometry("450x300+200+200")
    gui.title("HexChat Downloader GUI")
    
    editPackButton = Button(gui, text="Edit Packs", width=20, command=editPacks)
    editPackButton.pack(side="bottom", padx=70, pady=15)

    gui.mainloop()
    
def editPacks():
    print "Yahallo!"

#test

guiStart()