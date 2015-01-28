### This includes the functions:
### getint(), getcolor(), changesecret(), quitgame()

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random


### The main window (for some reason the app works best if this is here)
root = Tk()
root.wm_title("BRAINLORD")
root.minsize(200,360)



### Color reference for code and guesses
colorlist = ['white','red', 'orange', 'yellow', 'green', 'blue', 'purple']
def getint():
    return random.randint(1,6)
def getcolor():
    return colorlist[getint()]



### All-purpose quitting function
def quitgame():
    if messagebox.askokcancel("Quit", "Really quit the game?"):
        root.destroy()
