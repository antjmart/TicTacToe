class BoardClass:
    """A class that stores and handles information of the gameboard, stats, and players.

    Attributes:
        player1Name (str): The user name of player1. (Required parameter)
        player2Name (str): The user name of player2. (Required parameter)
        lastPlayer (str): The user name of the last player to have a turn.
        numWins (int): The total number of wins for this player.
        numTies (int): The total number of ties for this player.
        numLosses (int): The total number of losses for this player.
        numGames (int): The total number of games played.
        gameBoard (list[list[str, str, str], list[str, str, str], list[str, str, str]]): 3x3 grid of lists to represent the game board.
    """

    def __init__(self, player1Name: str, player2Name: str, lastPlayer: str = "", numWins: int = 0, numTies: int = 0, numLosses: int = 0, numGames: int = 0,
                 gameBoard: list[list[str, str, str], list[str, str, str], list[str, str, str]] = [["", "", ""], ["", "", ""], ["", "", ""]]):
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.lastPlayer = lastPlayer
        self.numWins = numWins
        self.numTies = numTies
        self.numLosses = numLosses
        self.numGames = numGames
        self.gameBoard = gameBoard

    def getPlayer1Name(self) -> str:
        """Get the user name of player1.

        Returns: A copy of player1's user name string.
        """
        return self.player1Name

    def getPlayer2Name(self) -> str:
        """Get the user name of player2.

        Returns: A copy of player2's user name string.
        """
        return self.player2Name

    def getLastPlayer(self) -> str:
        """Get the user name of the last player to take a turn.

        Returns: A copy of the last player's user name string.
        """
        return self.lastPlayer

    def getGameBoardTile(self, tile: int) -> str:
        """Get the current string value of a certain tile from the gameboard.

        tile: An integer ranging from 1-9 that denotes the tiles on the gameboard

        Returns: The string value of the corresponding gameboard tile
        """
        if 1 <= tile <= 3:
            # first row of board
            return self.gameBoard[0][tile - 1]
        elif 4 <= tile <= 6:
            # second row of board
            return self.gameBoard[1][tile - 4]
        else:
            # third row of board
            return self.gameBoard[2][tile - 7]
    
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

        Tile: Integer ranging from 1 to 9 that specifies a tic-tac-toe tile from top-left to bottom-right.
        gameLetter: Either X or O to represent what letter should be placed on the board.
        """
        if 1 <= tile <= 3:
            # first row of board
            self.gameBoard[0][tile - 1] = gameLetter
        elif 4 <= tile <= 6:
            # second row of board
            self.gameBoard[1][tile - 4] = gameLetter
        else:
            # third row of board
            self.gameBoard[2][tile - 7] = gameLetter

    def isWinner(self, playerLetter: str) -> bool:
        """Check the board if a win, with 3 of the same game piece aligned, has occurred.

        playerLetter: The letter that the player is using to play, either X or O.

        If win has occured, adds 1 to wins if this player won, adds 1 to losses if the other player won.
        Returns true or false regarding if a player did indeed win.
        """
        playerWon = False
        letter = None

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
            else:
                self.numLosses += 1

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

        return isFull

    def computeStats(self) -> str:
        """Compute each stat by pulling from BoardClass attributes and constructing them into individual strings.

        Returns: A condensed, concatenated string of all of the individual stat strings.
        """
        player1Stat = f"Player 1:  {self.player1Name}\n"
        player2Stat = f"Player 2:  {self.player2Name}\n"
        gamesStat = f"Number of games:  {self.numGames}\n"
        winsStat = f"Number of wins:  {self.numWins}\n"
        lossStat = f"Number of losses:  {self.numLosses}\n"
        tiesStat = f"Number of ties:  {self.numTies}"
        
        return player1Stat + player2Stat + gamesStat + winsStat + lossStat + tiesStat
