# BrainLord
A colorful code-breaking game based on the classic board game "MasterMind"

#### Anjana Vakil
20 December 2012

### Running the game:

	Clone the repository or download and expand the `.zip` archive, and move into the resulting `brainlord` directory.
	
	Then, to run the game, simply run the script "game_driver.py" with Python 3.
	
	For example:
		```
		Anjanas-MacBook-Air:Sheet6 Anjana$ python3 game_driver.py
		```

	This will launch the GUI for the game. 
	
	Use the buttons to navigate, and read the rules to learn how to play.

### Modules & other files:

	The following files contain necessary classes and functions 
	and must be in the same directory as "game_driver.py":
		- BLapp.py
		- board.py
		- functions.py
		- pegs.py
		- row.py
		
	Please see the comments in each of these files for more information.
	
	The following file lists the game rules, and must also be in the same directory:
		- rules.txt 

	The game stores all the player names and scores in the file:
		- scores.txt
	The first time the game is played in the given directory, this file will be created.
	After that, the app will read the "scores.txt" file and display the high scores
	on the "High Scores" page.
	Deleting this file will erase all the scores in the game's memory.
	
### Have fun, thanks for playing!
