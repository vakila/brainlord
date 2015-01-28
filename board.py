### This includes the class:
### Board

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random

from functions import *
from pegs import *
from row import Row

class Board:
    def __init__(self, parent, frame):
        ### Useful info for some methods
        self.parent = parent
        self.parentframe = frame

        ### Initially, display the game options panel (name & difficulty)
        self.options = Frame(self.parentframe, pady=20)
        self.options.pack(side=TOP, fill=Y, expand=1)

        ### Player enters name
        self.nameframe = LabelFrame(self.options, text="Enter Your Name",
                               labelanchor=N, padx=5, pady=5)
        self.nameframe.pack()
        self.playervar = StringVar()
        self.playervar.set("???")
        self.askname = Entry(self.nameframe, textvariable = self.playervar)
        self.askname.pack()

        Label(self.options).pack() #spacer
        
        ### Player chooses # of rows and duplicates option
        self.diff = LabelFrame(self.options, text="Select Difficulty Level",
                               labelanchor=N, padx=5, pady=5)
        self.diff.pack()
        self.numrowsvar = IntVar()
        Radiobutton(self.diff, text="Easy (12 rows)",
                           variable=self.numrowsvar, value=12).pack(anchor=W)
        Radiobutton(self.diff, text="Normal (10 rows)",
                           variable=self.numrowsvar, value=10).pack(anchor=W)
        Radiobutton(self.diff, text="Hard (8 rows)",
                           variable=self.numrowsvar, value=8).pack(anchor=W)
        self.numrowsvar.set(10)

        Label(self.diff).pack() #spacer

        self.dupvar = BooleanVar()
        self.dupvar.set(False)
        Checkbutton(self.diff,
                    text="Allow duplicates in the code (harder)",
                    variable= self.dupvar,
                    onvalue=True, offvalue=False).pack(anchor=W)


        Label(self.options).pack() #spacer


        ### Button to store name/difficulty & start the game
        Button(self.options, text="OK, let's play!",
               command=self.submitoptions).pack()
        
    def submitoptions(self):
        '''Stores player choices and starts the game'''
        ### Store the info from options pane as attributes
        self.player = self.playervar.get()
        self.numrows = self.numrowsvar.get()
        self.duplicates = self.dupvar.get()

        ### Replace options pane with main game board
        self.options.destroy()
        self.drawboard()

    def pick_secretcode(self):
        '''
        Selects a secret code, with or without duplicates
        as decided by player.
        '''
        if self.duplicates:
            self.secret_code = [getint(), getint(), getint(), getint()]
            self.dups = "duplicates allowed"
        else:
            self.secret_code = []
            for i in range(4):
                new = getint()
                while new in self.secret_code:
                    new = getint()
                self.secret_code.append(new)
            self.dups = "no duplicates"
                
    def drawboard(self):
        '''Draws the peg board for the current game'''
        ### Choose secret code
        self.pick_secretcode()
        #print("secret_code:", self.secret_code)

        ### Initialize score 
        self.score = 0

        ### Show player info and options above the board
        self.header = Frame(self.parentframe, pady = 10)
        self.header.pack()
        Label(self.header, text="{} vs. Computer".format(self.player)).pack()
        Label(self.header,
              text="{} rows, {}".format(self.numrows, self.dups)).pack()
        Label(self.header, text="Good Luck!").pack()
        
        ### Make board container    
        self.boardarea = Frame(self.parentframe, bg="gray", width=240,
                               borderwidth=5, relief=RAISED)
        self.boardarea.pack()

        ### Draw top row including secret pegs and "reveal" button
        self.toprow = Frame(self.boardarea, height=40, width=240, bg="gray")
        self.toprow.pack(side=TOP)
        self.toprow.pack_propagate(0)
        self.secretpegframe = Frame(self.toprow, width=160)
        self.secretpegframe.pack(side=LEFT)
        self.secretpegs = []
        for secretdigit in self.secret_code:
            self.secretpegs.append(SecretPeg(self.secretpegframe, secretdigit))
        self.revealframe = Frame(self.toprow, height=40, width=80, bg="gray")
        self.revealframe.pack(side=RIGHT)
        self.revealframe.pack_propagate(0)
        self.revealbutton = Button(self.revealframe, borderwidth=0, bg="gray",
                                   text="Reveal", command=self.forfeit)
        self.revealbutton.pack(side=LEFT, fill=X, expand=1)

        ### Make the number of rows chosen by player
        self.myrows = []
        for i in range(self.numrows):
            newrow = Row(self, self.boardarea, i)
            self.myrows.append(newrow)

        ### Activate the first (=bottom) row 
        self.myrows[0].activate()

    def advance_row(self):
        '''Moves play to the next row after a guess has been submitted'''
        thisrow = self.myrows[rownum]
        for peg in thisrow.mypegs:
            peg.canvas.unbind("<ButtonPress-1>")
        if rownum < (len(self.myrows)-1):
            nextrow = self.myrows[rownum+1]
            nextrow.activate()
            
    def revealall(self):
        '''If the player hits the "Reveal" button, reveals secret code'''
        for peg in self.secretpegs:
            peg.revealcolor()

    def forfeit(self):
        '''Checks that the player really wants to reveal the code'''
        if messagebox.askokcancel("Quitters Never Win",
                                  "Forfeit the game and reveal the secret code?"):
            self.revealall()
            ### Ask if the player wants another game
            self.parent.anothergame()
        




