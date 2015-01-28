### Import Everything ###

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random

from functions import *
from pegs import *
from row import Row
from board import Board
from BLapp import BLApp


### Run the Game ###
def main():
    print("Launching game window...")
    app = BLApp(root)
    root.mainloop()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
