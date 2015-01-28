### This contains the class:
### BLApp

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random

from functions import *
from pegs import *
from row import Row
from board import Board

class BLApp:
    def __init__(self, parent):
        '''Starts the app at the main menu (see self.mainmenu())'''
        self.parent = parent
        self.mainmenu()
        self.game = None # this is just here to avoid bug


    ### Some useful buttons & their commands
    def quitbutton(self, frame, packside=BOTTOM):
        # See "functions.py" for the quitgame() function
        self.quit = Button(frame, text="Quit", width=10, command=quitgame)
        self.quit.pack(side=packside)
    
    def homebutton(self, frame, packside=BOTTOM):
        self.home = Button(frame, text="Main Menu", width=10,
                           command=self.returnmenu)
        self.home.pack(side=packside)
    
    def returnmenu(self):
        if self.currentframe == self.game:
            if not messagebox.askokcancel("Abandon game",
                        """Abandon this game and return to the main menu?"""):
                return None
        self.currentframe.destroy()
        self.mainmenu()

    def makebuttonarea(self):
        '''Adds the Main Menu/Quit buttons to a page'''
        self.buttonarea = Frame(self.currentframe, pady=10)
        self.buttonarea.pack(side=BOTTOM)
        self.quitbutton(self.buttonarea,RIGHT)
        self.homebutton(self.buttonarea,LEFT)

    ### Create the main menu page
    def mainmenu(self):
        self.main = Frame(self.parent)
        self.main.pack()
        self.currentframe = self.main

        self.welcome = Label(self.main, text="Welcome to\nBRAINLORD")
        self.welcome.pack()
        self.drawlogo()
        self.letsplay = Button(self.main, text="New Game",
                               width=10, command=self.newgame)
        self.letsplay.pack()
        self.rules = Button(self.main, text="Rules",
                            width=10, command=self.go_rulespage)
        self.rules.pack()
        self.scores = Button(self.main, text="High Scores",
                             width=10, command=self.go_scorespage)
        self.scores.pack()
        self.quitbutton(self.main)
        
    def drawlogo(self):
        self.logo = Canvas(self.main, width=105, height=255)
        self.logo.pack()
        x = [(5,30),(30,55),(55,80),(80,105)]
        y = [(5,30),(30,55),(55,80),(80,105),(105,130),\
             (130,155),(155,180),(180,205),(205,230),(230,255)]
        for ycoords in y:
            y0 = ycoords[0]
            y1 = ycoords[1]
            for xcoords in x:
                x0 = xcoords[0]
                x1 = xcoords[1]
                self.logo.create_oval(x0,y0,x1,y1, fill=getcolor())

        


    ### Show the high scores page
    def scorespop(self):
        self.scorespop = Toplevel()
        self.scorespop.title = "High Scores"
        self.showscores(self.scorespop)

    def go_scorespage(self):
        ### Change current frame
        self.currentframe.destroy()
        self.scoresframe = Frame(self.parent, pady=10)
        self.scoresframe.pack(fill=Y, expand=1)
        self.currentframe = self.scoresframe
        ### Display scores
        self.showscores(self.scoresframe)
        ### Menu/Quit buttons
        self.makebuttonarea()
        
    def showscores(self, frame):
        '''This reads the file "scores.txt" and displays the top 10 scores.'''
        ### Area for top scores to be displayed
        self.scoresgroup = LabelFrame(frame,
                                      text="High Scores",
                                      labelanchor = N,
                                      padx=10)
        self.scoresgroup.pack(side=TOP, fill=Y, expand=1)
        self.scoresheader = Label(self.scoresgroup, text="(Rank, Name, Score)")
        self.scoresheader.pack()
        rawscores = []

        ### Try to open and read the scores file...
        try:
            with open("scores.txt", 'r') as scoresfile:
                for line in scoresfile:
                    line = line.strip()
                    name, score = line.split()
                    rawscores.append((name, int(score)))
 
        ### ...but don't freak out if it doesn't exist (see next block)
        except IOError:
            pass

        ### If scores file doesn't exist or is empty, display "no scores" msg
        if len(rawscores) == 0:
            self.noscores = Label(self.scoresgroup, pady=10,
                                  text="No scores in memory!",)
            self.noscores.pack()

        ### Otherwise, sort the scores and display the first 10 in order
        else:
            scores = sorted(rawscores, key=lambda x:x[1])
            self.top = scores[:10]
            for i in range(len(self.top)):
                topname = self.top[i][0]
                topscore = str(self.top[i][1])
                scoreline = str(i+1) + '.\t' + topname + '\t' + topscore
                Label(self.scoresgroup, text=scoreline, pady=5).pack(side=TOP)

    ### Show the rules
    def rulespop(self):
        self.rulespop = Toplevel()
        self.rulespop.title = "Rules"
        self.showrules(self.rulespop)

    def go_rulespage(self):
        self.currentframe.destroy()
        self.rulesframe = Frame(self.parent, pady=10, padx=10)
        self.rulesframe.pack()
        self.currentframe = self.rulesframe
        ### Display rules
        self.showrules(self.rulesframe)
        ### Menu/Quit buttons
        self.makebuttonarea()

    def showrules(self, frame):
        ### Area for displaying the rules
        self.rulesgroup = LabelFrame(frame,
                                     text= "Game Rules",
                                     labelanchor = N,
                                     padx = 10)
        self.rulesgroup.pack()

        ### Display the rules, reading from rules.txt file
        with open("rules.txt", 'r') as rulesfile:
            readall = rulesfile.read()
            readall = readall.split("\n\n\n")
            obj = readall[0]
            play = readall[1]
            sco = readall[2]
            #print(obj, play, sco, sep="\n\n\n")
            for chunk in readall:
                newline = Label(self.rulesgroup,
                                text=chunk,
                                justify=CENTER,
                                pady=5)
                newline.pack(side=TOP)

    ### Ask at the end of a game if the player would like to play again
    def anothergame(self):
        '''asks the player if they would like to play again'''
        another = messagebox.askyesno(title="Game Over", message="Play again?")
        if another:
            self.currentframe.destroy()
            self.newgame()
        else:
            self.currentframe.destroy()
            self.mainmenu()



    ### Start a new game
    def newgame(self):
        '''This loads the main game board - see "board.py"'''
        ### Change to game frame
        self.currentframe.destroy()
        self.game = Frame(self.parent, height=400, padx=10)
        self.currentframe = self.game
        self.game.pack()

        ### New board
        self.board = Board(self, self.game)

        ### Draw the Main/Quit/Rules/Scores buttons
        self.buttonarea = Frame(self.game, pady=10)
        self.buttonarea.pack(side=BOTTOM)
        self.buttonrow1 = Frame(self.buttonarea)
        self.buttonrow1.pack(side = BOTTOM)
        self.quitbutton(self.buttonrow1,RIGHT)
        self.homebutton(self.buttonrow1,LEFT)
        self.buttonrow2 = Frame(self.buttonarea)
        self.buttonrow2.pack(side=BOTTOM)
        self.scoresbutton = Button(self.buttonrow2, text="High Scores",
                                   command = self.scorespop, width=10)
        self.scoresbutton.pack(side=RIGHT)
        self.rulesbutton = Button(self.buttonrow2, text="Rules",
                                  command = self.rulespop, width=10)
        self.rulesbutton.pack(side=LEFT)


