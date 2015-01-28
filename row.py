### This includes the class:
### Row

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random

from functions import *
from pegs import Peg, FeedbackPegs

class Row:
    ### Row of guessing & feedback pegs
    def __init__(self, parent, frame, rownum):
        ### Helpful info for some methods
        self.parent = parent
        self.app = self.parent.parent
        self.rownumber = rownum

        ### Main container 
        self.rowframe = Frame(frame, height=40, width=240, background="gray")
        self.rowframe.pack(side=BOTTOM)        

        ### Container for guessing pegs
        self.pegsframe = Frame(self.rowframe, width=160, bg="gray")
        self.pegsframe.pack(side=LEFT)
        self.peg1 = Peg(self.pegsframe, 1)
        self.peg2 = Peg(self.pegsframe, 2)
        self.peg3 = Peg(self.pegsframe, 3)
        self.peg4 = Peg(self.pegsframe, 4)
        self.mypegs = [self.peg1, self.peg2, self.peg3, self.peg4]

        ### Container for feedback pegs
        ### Displays empty "holes" until row is activated
        self.feedbackframe = Frame(self.rowframe, heigh=40, width=80,
                                   bg="gray", highlightthickness=0)
        self.feedbackframe.pack(side=RIGHT)
        self.feedbackframe.pack_propagate(0)
        self.dummypegs = Canvas(self.feedbackframe, width=40, height=40,
                                bg="gray", highlightthickness=0)
        self.dummypegs.pack()
        self.dummypegs.create_oval(9,9,19,19, fill="gray")
        self.dummypegs.create_oval(21,9,31,19, fill="gray")
        self.dummypegs.create_oval(9,21,19,31, fill="gray")
        self.dummypegs.create_oval(21,21,31,31, fill="gray")


    def activate(self):
        '''Makes the row active for guessing'''
        ### Make pegs clickable
        for peg in self.mypegs:
            peg.canvas.bind("<ButtonPress-1>", peg.changecolor)

        ### Destroy empty feedback peg holes & create "submit" button
        self.dummypegs.destroy()
        self.submitbutton = Button(self.feedbackframe, text = "Submit!",
                                   command=self.submitguess, bg="gray")
        self.submitbutton.pack(side=LEFT, fill=X, expand=1)

    def deactivate(self):
        '''Deactivates the row after a guess has been made'''
        ### Make pegs unclickable
        for peg in self.mypegs:
            peg.canvas.unbind("<ButtonPress-1>")

        ### If the guess for this row is correct, game is over
        if self.myfeedback == [2,2,2,2]:
            #print("score:", self.parent.score)
            self.gameover(result="WIN")

        ### Otherwise, if the top row has been reached, game is lost
        elif self.rownumber == (self.parent.numrows - 1):
            self.parent.score += 1
            #print("score:", self.parent.score)
            self.gameover()
        
        ### Otherwise, game continues and next row is activated
        else:
            nextrow = self.parent.myrows[self.rownumber + 1]
            nextrow.activate()
            self.parent.score += 1
            #print("score:", self.parent.score)


    def gameover(self, result="LOSE"):
        '''Ends the current game'''
        ### Reveal the secret
        self.parent.revealall()
        self.parent.revealbutton.destroy()

        ### Add score to scores.txt file
        ### (if the file doesn't exist yet, it is created)
        thisplayer = self.parent.player
        thisscore = str(self.parent.score)
        with open("scores.txt", 'a') as scoresfile:
                newline = thisplayer + " " + thisscore + '\n'
                scoresfile.write(newline)

        ### Display Gameover message with Score
        winlose = "YOU " + result + "!!!"
        scoremsg = "Your score: " + str(self.parent.score)
        gameovermsg = winlose + '\n' + scoremsg
        messagebox.showinfo(title="Game Over", message = gameovermsg)

        ### Ask for new game Y/N
        self.app.anothergame()
        

    def submitguess(self):
        '''Submit the guess for feedback'''
        self.myguess = [peg.value for peg in self.mypegs]
        if 0 in self.myguess:
            messagebox.showerror(title="Guess Again", message="You must choose a color for each peg!")
            return None
        self.submitbutton.destroy()
        #print("row#:", self.rownumber, "guess:", self.myguess)
        self.myfeedback = self.checkguess()
        
        self.feedbackpegs = FeedbackPegs(self.feedbackframe, self.myfeedback)
        self.deactivate()
        #return self.myguess
        

    def checkguess(self):
        '''
        Compares the guess for this row to the secret code.
        Returns a "feedback list" of four ints that is used to
        display the correct feedback pegs (see "pegs.py").
        '''
        target = self.parent.secret_code[:] #shallow copy is OK since list is all ints
        guess = self.myguess #shared ref OK since not changing
        feedbacklist = []
        nojoy = []
        
        if guess == target:
            feedbacklist = [2,2,2,2]
            return feedbacklist
        
        for i in range(0,4):
            if guess[i] == target[i]:
                feedbacklist.append(2)
                target[i] = "done"
            else:
                nojoy.append(guess[i])
        for i in range(len(nojoy)):
            if nojoy[i] in target:
                feedbacklist.append(1)
                target.remove(nojoy[i])
            else:
                feedbacklist.append(0)
        return feedbacklist
        
    
