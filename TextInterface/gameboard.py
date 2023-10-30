class InvalidMove(Exception):
    """Custom exception made to classify a move that cannot be made (tile space already with a letter).
    """
    pass

class BoardClass:
    """A class that stores and handles information of the gameboard, stats, and players.

    Attributes:
        playerName (str): The user name of the player with this game board. (Required parameter)
        otherPlayer (str): The user name of the other tic-tac-toe player.
        lastPlayer (str): The user name of the last player to have a turn.
        numWins (int): The total number of wins for this player.
        numTies (int): The total number of ties for this player.
        numLosses (int): The total number of losses for this player.
        numGames (int): The total number of games played.
        gameBoard (list[list[str, str, str], list[str, str, str], list[str, str, str]]): 3x3 grid of lists to represent the game board.
    """

    def __init__(self, playerName: str, otherPlayer: str = "", lastPlayer: str = "", numWins: int = 0, numTies: int = 0, numLosses: int = 0, numGames: int = 0,
                 gameBoard: list[list[str, str, str], list[str, str, str], list[str, str, str]] = [["", "", ""], ["", "", ""], ["", "", ""]]):
        self.playerName = playerName
        self.otherPlayer = otherPlayer
        self.lastPlayer = lastPlayer
        self.numWins = numWins
        self.numTies = numTies
        self.numLosses = numLosses
        self.numGames = numGames
        self.gameBoard = gameBoard

    def getPlayerName(self) -> str:
        """Get the user name of the player with this game board.

        Returns: A copy of the player's user name string.
        """
        return self.playerName

    def getOtherPlayer(self) -> str:
        """Get the user name of the opposing player.

        Returns: A copy of the opposing player's user name string.
        """
        return self.otherPlayer
    

    def setOtherPlayer(self, otherName: str) -> None:
        """Set the user name of the opposing player attribute.

        otherName: String representing the username of the opposing player.
        """
        self.otherPlayer = otherName

    def setLastPlayer(self, userName: str) -> None:
        """Set the user name of the last player to have a turn.

        userName: String representing the username of the last player to have a turn.
        """
        self.lastPlayer = userName
        

    def updateGamesPlayed(self) -> None:
        """Updates number of games started by incrementing numGames by 1.
        """
        self.numGames += 1

    def resetGameBoard(self) -> None:
        """Reset the game board by replacing all parts of the grid with empty strings.
        """
        for i in range(3):
            for j in range(3):
                self.gameBoard[i][j] = ""
            
    def updateGameBoard(self, tile: int, gameLetter: str) -> None:
        """Replace specified board tile (1 - 9) with an X if player 1, O if player 2.

        Tile: Integer ranging from 1 - 9 that specifies a tic-tac-toe tile from top-left to bottom-right.
        gameLetter: Either X or O to represent what letter should be placed on the board.
        """
        if 1 <= tile <= 3:
            # first row of board
            if self.gameBoard[0][tile - 1] == "":
                self.gameBoard[0][tile - 1] = gameLetter
            else:
                raise InvalidMove
        elif 4 <= tile <= 6:
            # second row of board
            if self.gameBoard[1][tile - 4] == "":
                self.gameBoard[1][tile - 4] = gameLetter
            else:
                raise InvalidMove
        else:
            # third row of board
            if self.gameBoard[2][tile - 7] == "":
                self.gameBoard[2][tile - 7] = gameLetter
            else:
                raise InvalidMove

    def isWinner(self, playerLetter: str) -> bool:
        """Check the board if a win, with 3 of the same game piece aligned, has occurred.

        playerLetter: The letter that the player is using to play, either X or O.

        If win has occurred, adds 1 to wins if this player won, adds 1 to losses if the other player won.
        Returns true or false regarding if a player did indeed win.
        """
        playerWon = False
        
        for i in range(3):
            if (self.gameBoard[i][0] != "") and (self.gameBoard[i][0] == self.gameBoard[i][1]) and (self.gameBoard[i][1] == self.gameBoard[i][2]):
                # checks for the same 3 letters on the rows
                playerWon = True
                letter = self.gameBoard[i][0]
            elif (self.gameBoard[0][i] != "") and (self.gameBoard[0][i] == self.gameBoard[1][i]) and (self.gameBoard[1][i] == self.gameBoard[2][i]):
                # checks for the same 3 letters on the columns
                playerWon = True
                letter = self.gameBoard[0][i]

        if (self.gameBoard[0][0] != "") and (self.gameBoard[0][0] == self.gameBoard[1][1]) and (self.gameBoard[1][1] == self.gameBoard[2][2]):
                # checks for the same 3 letters on the top left to bottom right diagonal
                playerWon = True
                letter = self.gameBoard[1][1]
        elif (self.gameBoard[2][0] != "") and (self.gameBoard[2][0] == self.gameBoard[1][1]) and (self.gameBoard[1][1] == self.gameBoard[0][2]):
                # checks for the same 3 letters on the bottom left to top right diagonal
                playerWon = True
                letter = self.gameBoard[1][1]

        if playerWon:
            if playerLetter == letter:
                self.numWins += 1
                print("You won!")
            else:
                self.numLosses += 1
                print("You lost...")

            self.updateGamesPlayed()

        return playerWon

    def boardIsFull(self) -> bool:
        """Check if the board is filled up, with no possible moves to be made.

        If this is true, updates total number of ties.
        Returns true or false if the board is indeed filled up.
        """
        isFull = True

        # if there are any empty spaces, the board is deemed not full
        for row in self.gameBoard:
            for space in row:
                if space == "":
                    isFull = False
        if isFull:
            self.numTies += 1
            self.updateGamesPlayed()
            print("Tie!")

        return isFull

    def printStats(self) -> None:
        """Print out each of this game board's attributes on a newline.
        """
        print("Player's user name:", self.playerName)
        print("Last player to make a move:", self.lastPlayer)
        print("Number of games played:", self.numGames)
        print("Number of wins:", self.numWins)
        print("Number of losses:", self.numLosses)
        print("Number of ties:", self.numTies)

    def printBoard(self) -> None:
        """Print out a formatted 3x3 visual grid of the game board.
        """
        print(f'\n{self.gameBoard[0][0]:^3}|{self.gameBoard[0][1]:^3}|{self.gameBoard[0][2]:^3}')
        print('-' * 11)
        print(f'{self.gameBoard[1][0]:^3}|{self.gameBoard[1][1]:^3}|{self.gameBoard[1][2]:^3}')
        print('-' * 11)
        print(f'{self.gameBoard[2][0]:^3}|{self.gameBoard[2][1]:^3}|{self.gameBoard[2][2]:^3}\n')

    def printInstructions(self) -> None:
        """Print out instructions for what numbers (1-9) correspond to which tile on the gameboard, using a 3x3 grid.
        """
        print("Moves are made with an integer from 1-9, following the format of the grid below.")
        print(f'{1:^3}|{2:^3}|{3:^3}')
        print('-' * 11)
        print(f'{4:^3}|{5:^3}|{6:^3}')
        print('-' * 11)
        print(f'{7:^3}|{8:^3}|{9:^3}\n')
