#### This includes the classes: 
#### Peg, SecretPeg, FeedbackPegs

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random

from functions import *

### Pegs for player's guesses
class Peg:
    #Creates a single peg that will cycle through colors when clicked.
    def __init__(self, frame, pegnum):
        self.value = 0
        self.id = pegnum
        self.canvas = Canvas(frame, width=40, height=40, bg="gray",
                             highlightthickness=0)
        self.canvas.pack(side = LEFT)
        self.canvas.create_oval(5,5,35,35, fill="gray")
        
    def changecolor(self, x=None):
        # x is dummy variable b/c 2 arguments get passed to self.changecolor()
        # I don't know why that is, but it works :)
        if self.value == 6:
            self.value = 1
        else:
            self.value += 1
        newcolor = colorlist[self.value]
        self.canvas.create_oval(5,5,35,35, fill=newcolor)



### Pegs for the secret code
class SecretPeg:
    # Creates a single peg with a given (hidden) color
    def __init__(self, frame, secretdigit):
        self.value = secretdigit #self.secret_code[pegnum]
        self.color = colorlist[self.value]
        self.canvas = Canvas(frame, width=40, height=40, bg="gray",
                             highlightthickness=0)
        self.canvas.pack(side=LEFT)
        self.canvas.create_oval(5,5,35,35, fill="black")
        self.canvas.create_text(20,20, fill="white", text="?")

    def revealcolor(self, x=None):
        self.canvas.create_oval(5,5,35,35, fill=self.color)



### Little pegs for feedback on the player's guesses      
class FeedbackPegs:

    def __init__(self, frame, feedbacklist):
        self.canvas = Canvas(frame, width=40, height=40, bg="gray",
                             highlightthickness=0)
        self.canvas.pack()
        self.respond(feedbacklist)

    def respond(self, feedbacklist):
        # feedbacklist is a list of 4 integers (0-2), e.g. [1,0,2,1],
        # the numbers indicate the correctness of the guess
        colors = ["gray", "white", "black"]
        hardfeedback = sorted(feedbacklist, reverse=True)
        self.canvas.create_oval(9,9,19,19, fill= colors[hardfeedback[0]])
        self.canvas.create_oval(21,9,31,19, fill= colors[hardfeedback[1]])
        self.canvas.create_oval(9,21,19,31, fill= colors[hardfeedback[2]])
        self.canvas.create_oval(21,21,31,31, fill= colors[hardfeedback[3]])

