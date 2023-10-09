import random,sys,time

# _______________________________________________________________________________________________
# PLEASE READ
# - Intermediate and expert will not display correctly unless you run the file in fullscreen in Python / CLI. (NOT VSC)
# - Expert has been changed to 16 x 16 as 30 x 16 will not run.
# - Do not run the file if leaderboard.txt is open.
# - Do not change the format of the contents in the leaderboard.txt file.
# _______________________________________________________________________________________________


# Creating an empty list to store the leaderboard in
Leaderboard = []


# Opening and writing the contents of the leaderboard to the list. If the file doesnt exist, it is created.
try:
    Leaderboard_File = open("leaderboard.txt")
    File = Leaderboard_File.read()
    Leaderboard = File.split("\n")
except FileNotFoundError:
    Leaderboard_File = open("leaderboard.txt","w+")
Leaderboard_File.close()


# Creating a list containing the 10 digits. This will be used to check that the user has actually inputted numbers during the game.
Numbers = ["0","1","2","3","4","5","6","7","8","9"]

# Creating a list to store bomb locations in.
Bomb_Locations = []

# Integer that counts how many hints have been used.
Hints_Remaining = 0

# Defining the game variable beforehand so it can be used anywhere in the program.
global Game


# The class for the game board.
class Game_Board:
    def __init__(self, Difficulty):

        # Initialising variables for the timer to function
        self.Start_Time = 0
        self.Stop_Time = 0 

        # Setting the board size and number of bombs based on difficulty
        if Difficulty == 1:
            # Beginner
            self.Board_Rows = 9
            self.Board_Columns = 9
            self.Bomb_Amount = 10
            self.Difficulty = "Beginner"
        elif Difficulty == 2:
            # Intermediate - Will not display correctly unless running in full screen Python / CLI
            self.Board_Rows = 16
            self.Board_Columns = 16
            self.Bomb_Amount = 40
            self.Difficulty = "Intermediate"
        elif Difficulty == 3:
            # Expert - Will not run if the rows / columns value is 30. Returns a list index error.
            self.Board_Rows = 16
            self.Board_Columns = 16
            self.Bomb_Amount = 99
            self.Difficulty = "Expert"

        # Setting the amount of hints remaining to the amount of bombs.
        global Hints_Remaining
        Hints_Remaining = self.Bomb_Amount

        # Creating a list to store the board in
        self.Board = [['' for Row in range(self.Board_Rows)] for Column in range(self.Board_Columns)]

        # Creating a list to store the tiles that have been uncovered already
        self.Uncovered_Tiles = [[False for Row in range(self.Board_Rows)] for Column in range(self.Board_Columns)]

        # Creating a list to store tiles the user has flagged
        self.Flagged_Tiles = [[False for Row in range(self.Board_Rows)] for Column in range(self.Board_Columns)]

        # Flagged bombs counter, when this reaches the number of bombs in the field the user wins
        self.Flagged_Bombs = 0

        # Available flags counter: the user can only flag as many tiles as there are bombs available to prevent them from flagging every tile and winning.
        self.Available_Flags = self.Bomb_Amount

        # Boolean that keeps track of if the user has lost or not
        self.Lost = False         

                                                                            
        # Placing the bombs
        Bombs_Placed = 0
        while Bombs_Placed < self.Bomb_Amount:                                              # Will keep placing bombs until the bomb counter (amount of bombs placed) reaches the amount of bombs to be placed for this difficulty
            Bomb_Location = random.randint(0, self.Board_Rows*self.Board_Columns -1)        # Randomly determining a bomb location within the bounds of the board
            Bomb_Row = Bomb_Location // self.Board_Rows                                     # Finding the actual index of the row of the bomb to be placed
            Bomb_Column = Bomb_Location % self.Board_Columns                                # The same but for the column
            if Bomb_Column > self.Board_Columns:
                Bomb_Column = self.Board_Columns - 1

            if self.Board[Bomb_Row][Bomb_Column] != "*":                                    # If the tile does not have a bomb in it, place one
                self.Board[Bomb_Row][Bomb_Column] = "*"
                Bomb_Row = Bomb_Row + 1                                                     # Adding one to offset the index
                Bomb_Column = Bomb_Column + 1
                Bomb_Row = str(Bomb_Row)
                Bomb_Column = str(Bomb_Column)
                String = (Bomb_Row,Bomb_Column)                                             # Converting the bomb coordinates to a string
                Bomb_Locations.append(String)                                               # Adding the bomb to the list of bomb locations
                Bombs_Placed = Bombs_Placed + 1                                             
        #print(self.Board)                                                                  # Debug - will print the board with bombs inside

        # Finding which tiles to assign clue numbers to
        for Row in range(self.Board_Rows):
            for Column in range(self.Board_Columns):                                      
                if self.Board[Row][Column] != "*":                                          # If this tile is not a bomb, pass the row and column of the tile and call Tile_Clue so the correct number can be found
                    self.Board[Row][Column] = self.Tile_Clue(Row, Column)
        
        #print(self.Board)                                                                  # Debug - will print the board with bombs and tile clues inside
        

    # Function to assign the clue number for each tile
    def Tile_Clue(self, Tile_Row, Tile_Column):
        
        Surrounding_Bombs = int(0)                                                                          # Variable used to keep track of how many bombs are surrounding the tile

        for Row in range(max(0, Tile_Row - 1), min(self.Board_Rows - 1, Tile_Row + 1) + 1):
            for Column in range(max(0, Tile_Column - 1), min(self.Board_Columns - 1, Tile_Column + 1) + 1): # Searching the tiles surrounding the current tile being checked, ensuring that it is not out of bounds                                                                                                                  # If the tile is out of bounds, or the "surrounding" tile is actually the original / tile being checked, continue through the loop
                    #print("Current Row -", Row, "Column -", Column)
                    if self.Board[Row][Column]: 
                        if self.Board[Row][Column] == "*":                                                  # If the tile has a bomb, add one to the amount of bombs surrounding the tile being checked
                            Surrounding_Bombs = Surrounding_Bombs + 1
        
        return Surrounding_Bombs                                                                            # Return the amount of surrounding bombs to the __init__ function


    # Function that checks the tile the user has uncovered ONLY. If this tile was already uncovered, then it will show them a message. Otherwise, it will call the actual Uncover function.
    def Tile_Check(self, Row, Column):

        if self.Uncovered_Tiles[Row][Column] == True:
            print("\nYou've already uncovered this tile!")
            return
        else:
            self.Uncover(Row, Column)


    # Function for when the user decides to uncover a tile. Passed the row and column of the tile the user wants to uncover.
    def Uncover(self, Tile_Row, Tile_Column):

        self.Uncovered_Tiles[Tile_Row][Tile_Column] = True                                                  # Change the value in Uncovered_Tiles to True.
        
        #print("Uncovered = ", self.Uncovered_Tiles[Tile_Row][Tile_Column])
        #print("Space dug:", self.Board[Tile_Row][Tile_Column])                                             # Debugging

        if self.Board[Tile_Row][Tile_Column] == "*":                                                        # If the tile contains a bomb, end the game.
            self.Lost = True                                                                                # Variable signifying the user's loss - returned to the Minesweeper function
            return
        elif self.Board[Tile_Row][Tile_Column] > 0:                                                         # If the tile has a number on it, stop uncovering
            #print("Stopped digging. Tile is: Row -", Tile_Row, "Column -", Tile_Column, "Tile inside:", self.Board[Tile_Row][Tile_Column])
            return
            
                                                              
        for Row in range(max(0, Tile_Row - 1), min(self.Board_Rows - 1, Tile_Row + 1) + 1):                 # Check the tiles surrounding this tile and call the Uncover function recursively until a tile with a number has been uncovered. Makes sure that the indexes are not out of bounds.
            for Column in range(max(0, Tile_Column - 1), min(self.Board_Columns - 1, Tile_Column + 1) + 1):
                #print("Now checking the surrounding tile which is: Row -", Row, "Column -", Column)                                                                      
                if self.Uncovered_Tiles[Row][Column] == False:                                              # Will only call Uncover again if the tile was not uncovered before
                    #print("Inside this tile is:", self.Board[Row][Column])   
                    self.Uncover(Row, Column)       
        

    # Function that allows the user to flag a tile. Passed the row and column of the tile the user wants to flag.
    def Flag(self, Tile_Row, Tile_Column):

            if self.Uncovered_Tiles[Tile_Row][Tile_Column] == True:             # If this tile is already uncovered, do not flag it, and notify the user.
                print("\nYou can't flag that tile, it has already been uncovered!")               
            if self.Flagged_Tiles[Tile_Row][Tile_Column] == True:               # If the tile is already flagged, unflag it.
                self.Flagged_Tiles[Tile_Row][Tile_Column] = False
                self.Available_Flags = self.Available_Flags + 1                 # Adding one to the available flags if the user unflags a tile.
                if self.Board[Tile_Row][Tile_Column] == "*":                    # If the tile the user is unflagging is a bomb, subtract one from the Flagged_Bombs counter.
                    self.Flagged_Bombs = self.Flagged_Bombs - 1                        
            elif self.Available_Flags > 0:                                      # If the user has flags available, let them flag the tile.
                self.Flagged_Tiles[Tile_Row][Tile_Column] = True
                self.Available_Flags = self.Available_Flags - 1                 # Subtracting one to the available flags if the user flags a tile.
                if self.Board[Tile_Row][Tile_Column] == "*":
                    self.Flagged_Bombs = self.Flagged_Bombs + 1                 # If the tile the user is flagging is a bomb, add one to the Flagged_Bombs counter.
            elif self.Available_Flags == 0:                                     # If the user runs out of flags, do not let them flag athe tile and notify them.
                print("\nOut of flags! Unflag a space to get more.")


    # Function that gives the user a hint
    def Hint(self):

        global Hints_Remaining                                                          

        if Hints_Remaining == 0:                                                                            # If the user runs outof hints, dont let them use a hint and notify them.
            print("\nHmm... it seems you've used all of your hints. Try completing the level yourself!")
            return
        Bomb_Number = random.randint(0, (Hints_Remaining -1))                                               # Randomly chosing a number from 0 to Hints_Remaning minus one to account for indexing
        if Bomb_Number < 1:                                                                                 # If the number chosen ends up being less than one, the number will be changed to 0.
            Bomb_Number = 0
        #print("Bomb to be hint index:", Bomb_Number)                                                       # Debugging
        Hint_Bomb = Bomb_Locations[Bomb_Number]                                                             # The index just created acts as the location for the bomb in the list of bomb locations
        Bomb_Locations.pop(Bomb_Number)                                                                     # This bomb is then removed from the list, and 1 is subtracted from Hints_Remaining to reflect this
        Hints_Remaining = Hints_Remaining - 1
        print("\nHint used:\nBomb location - ",Hint_Bomb)                                                   # Gives he user the hint



    # Pre-provided function to print the game board. Slightly edited.
    def Print_Board(self):

        #Example of a function to print the board in the terminal. (Using this example is not obligatory)
        # Inputs:
        #        board: two-dimensional list that contains mines and clues
        #        is_cell_open: two-dimensional list containing True or False.
        #                       True in case the cell is opened by the player, False otherwise
        #        flagged_cells: two-dimensional list containing the cells that the user has flagged as mines

        print("\n_______________________________________________________________________\n")
        Num_Of_Rows = self.Board_Rows
        Num_Of_Columns = self.Board_Columns
        Columns_id  = range(0,Num_Of_Columns)
        print('\t',end='') # Required for proper visualization of the columns' id numbers
        for id in Columns_id: # Print the id numbers of columns
            print(id + 1,'\t',end='')  # the end='' prevents print to change line
        print('\n')
        for Board_Row in range(Num_Of_Rows):
            print(Board_Row + 1,'| ',end='') # Print the id numbers of rows
            for Board_Column in range (Num_Of_Columns):
                if self.Uncovered_Tiles[Board_Row][Board_Column] == True:# For each cell in the board, check if it is opened by the player
                    #if self.Board[Board_Row][Board_Column] == 0:
                        #print('\tO',end='')
                    #else:
                    print('\t', self.Board[Board_Row][Board_Column],end='')
                    if self.Flagged_Tiles[Board_Row][Board_Column] == True: # !If a flagged spot is uncovered, remove the flag and add one to available flags.!
                        self.Flagged_Tiles[Board_Row][Board_Column] = False
                        self.Available_Flags = self.Bomb_Amount - self.Flagged_Bombs
                elif self.Flagged_Tiles[Board_Row][Board_Column] == True: # if the cell is flagged as mine by the player print F
                    print('\tF', end='')
                else: # Print nothing if the cell is not open
                    print('\t-', end='')
            print('\n')
            

# Function that gets and stores the user's name.
def Get_Name():

    global Name

    Name = input("\n----- Welcome! -----\n\nBefore starting, please enter your name.\n\n")
    Main()


# The function that asks the user what difficulty they would like to play and passes this to Minesweeper. 
def Main():

        print("_______________________________________________________________________")
        Choice = (input("\n\nWelcome to minesweeper!\n\n\nPlease select your difficulty:\n\nBeginner - 1\nIntermediate - 2\nExpert - 3\nPlayer Stats - 4\nExit Game - 5\n\n"))
        try:
            Choice = int(Choice)
        except ValueError:
            print("\nInvalid input. Please make sure to just type the number of your choice.")
            Main()
        if Choice == 1 or Choice == 2 or Choice == 3:
            Minesweeper(Choice)
        elif Choice == 4:       # Statistics page
            Stats()
        elif Choice == 5:       # Exits the program
            sys.exit()
        else:
            print("\nInvalid input. Please make sure to just type the number of your choice.")
            Main()


# The function that allows the user to play the game. Passed the difficulty from Main.
def Minesweeper(Difficulty):

    global Game     

    Game = Game_Board(Difficulty)                                                                   # Initialising a Game object using the chosen difficulty

    Instructions()                                                                                  # Prints the instructions

    Game.Start_Time = time.time()                                                                   # Starts the game timer by getting the current time.
    
    while Game.Flagged_Bombs < Game.Bomb_Amount and Game.Lost == False:                             # Loop that handles the game. Once all bombs have been flagged, the game ends. The game also ends when a bomb is uncovered.

        time.sleep(1)
        Game.Print_Board()                                                                          # Prints the board
        print("_______________________________________________________________________")
        print("Flags available:", Game.Available_Flags,"\nUnflagged bombs:", Game.Bomb_Amount - Game.Flagged_Bombs, "\n")
        Choice = input("Please input your action:\n   -->  ")                                       # Gets user input
        if Choice == "":                                                                            # If the user inputs nothing, raise an error
            Invalid_Input()
            continue
        Choice = Choice.upper()                                                                     # Formats the input to all be upper-case
        
        if Choice == "EXIT":                                                                        # Exits the program
            sys.exit()
        elif Choice == "HELP":                                                                      # Prints the instructions
            Instructions()
            continue
        elif Choice == "HINT":
            Game.Hint()                                                                             # Gives the user a hint then continues through the loop
            continue
 
        Choice.replace(" ","")                                                                      # Removing any spaces from the user input
        # Input format: U1,2

        
        if Choice[0] == "U" or Choice[0] == "F":                                                    # Checking if the user correctly inputted U or F
            Action = Choice[0]                                                                      # Sets the Action variable as U or F
            Choice = Choice[1:]                                                                     # Removes the first character of the user's input
            if Choice[1] == "," or Game.Board_Rows > 9 and Choice[2] == "," :                                                                       
                Choice = Choice.split(",")                                                          # If a comma is present, creates a list, splitting the elements by the comma
                if len(Choice) > 2:                                                                 # If the list is longer than 2 elements, the input is invalid.
                    Invalid_Input()
                    continue
            else:                                                                                   # If no comma is present, the input is invalid.
                Invalid_Input()
                continue                                                       
            for Element in Choice:                                                                  # For the element in this new list, for every character, if this isnt a digit, then the input is invalid.                                    
                for Character in Element:
                    if Character in Numbers:
                        pass
                    else:
                        Invalid_Input()                                             
                        continue
            Row = int(Choice[0]) - 1
            Column = int(Choice[1]) - 1                                                             # Sets the row and column variables with offset for index
            #print("Action:", Action, "Row:", Row, "Column:", Column)
            if Row < 0 or Row > Game.Board_Rows or Column < 0 or Column > Game.Board_Columns:       # If the row and column inputted are out of bounds, the input is invalid.
                Invalid_Input()
                continue
            if Action == "U":                                                                       # Passes the row and column to Uncover
                Game.Tile_Check(Row, Column)
            elif Action == "F":                                                                     # Passes the row and column to Flag
                Game.Flag(Row, Column)
        else:                                                                                       # If the user didn't enter a U or F, the input is invalid.
            Invalid_Input()
            continue

    # Loop is broken out of
    if Game.Lost == False:      
        Game_Won()
    elif Game.Lost == True:
        Game_Over()


# Prints the game instructions.
def Instructions():

    print("_______________________________________________________________________")
    print("Instructions:\n")
    print("Uncover a tile: Reveal what is in a tile.\nFlag a tile: Flag a tile as a bomb. Flag an existing flag to remove it.\n")
    print("How to take an action:\nType the corresponding letter - Uncover (U) or Flag (F)\nfollowed by the coordinates of the tile in the format (Row,Column).\n")
    print("Example: U1,2 / F1,2\n")
    print("\nTo exit the game at any time, type 'Exit'.\nIf you would like to view these instructions again, type 'Help'.")
    input("\nPress enter to continue...")
    print("_______________________________________________________________________")


# Function that tells the user their input was invalid.
def Invalid_Input():
    print("\nInvalid input. Ensure your coordinates are within the bounds of the board, and that you are inputting using the correct format.\nIf you need help, type 'Help'.")


# Function that handles a game over (when the user uncovers a bomb)
def Game_Over():

    global Game

    Game.Uncovered_Tiles = [[True for Row in range(Game.Board_Rows)] for Column in range(Game.Board_Columns)]
    Game.Print_Board()

    print("_______________________________________________________________________")
    print("\nUh oh, you dug up a bomb!")
    print("_______________________________________________________________________")
    input("\nPress enter to return to the title screen to play again or exit!")
    Main()


# Function that handles winning the game
def Game_Won():

    global Game
    global Name

    Game.Stop_Time = time.time()
    End_Time = Game.Stop_Time - Game.Start_Time # Calculating the time taken to beat the game.
    Finish_Time = "{:.2f}".format(End_Time)

    Game.Uncovered_Tiles = [[True for Row in range(Game.Board_Rows)] for Column in range(Game.Board_Columns)]
    Game.Print_Board()
    
    # Updates the Leaderboard list
    Leaderboard.append(Name)
    Finish_Time = str(Finish_Time)
    Leaderboard.append(Finish_Time)
    Leaderboard.append(Game.Difficulty)

    # Writes the updated Leaderboard list to the text file
    String = ""
    for Element in Leaderboard:
        String = String+Element+"\n"
    Leaderboard_File = open("leaderboard.txt","w")
    Leaderboard_File.write(String)
    Leaderboard_File.close()

    print("_______________________________________________________________________")
    print("Congratulations! You won the game!")
    print(Name,", you took", Finish_Time, "seconds to clear", Game.Difficulty, "difficulty!")
    print("_______________________________________________________________________")
    input("\nPress enter to return to the title screen to play again or exit!")
    Main()


# Prints the player stats to the user
def Stats():

    print("\n_______________________________________________________________________")
    print("User Statistics:")

    Position = 0
    while True:
        try:
            if Leaderboard[Position+3]:                                                                                                 # Checks that the index exists                                                                                    
                print("\n-->",Leaderboard[Position+1],"\nTime:", Leaderboard[Position+2],"\nDifficulty:", Leaderboard[Position+3])      # Print out the stats for that player
                Position = Position + 4                                                                                                 # Then add 4 to position to move to the next player
        except IndexError:
            break                                                                                                                       # Breaks out of the loop if the index in line 424 does not exist
    
    print("_______________________________________________________________________")
    input("\nPress enter to return to the main menu or exit!")
    Main()


# Runs the start of the program
Get_Name()

