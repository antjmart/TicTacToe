from gameboard import BoardClass
import socket
import tkinter as tk

class player2UI():
    """A class that handles and processes the GUI aspects of the Tic-Tac-Toe game, for player2, using TKinter elements.

    Attributes:
        userName (str): The user name string for player2, alphanumeric only.
        s (socket): Socket type object that sets up the socket connection for the GUI.
        conn (socket): Socket type object that handles the GUI's socket connections.
        host (str): The host name or IP address of the intended device to connect to.
        port (int): The port number used to connect to the host.
        setupWindow (TK): Window used to host widgets for establishing username and socket connection information.
        root (TK): Main window used to display the Tic-Tac-Toe game.
        playerBoard (BoardClass): BoardClass type object that stores and processes all of the internal game information.
        canMove (bool): Determines if player2 can make a move, true if it is player2's turn.
    """
    
    def __init__(self):
        """Initialize the program by establishing the tkinter window setupWindow and its relevant widgets.
        """
        # creating and configuring the setupWindow
        self.setupWindow = tk.Tk()
        self.setupWindow.title("Tic-Tac-Toe (Player 2)")
        self.setupWindow.geometry('420x300+550+300')
        self.setupWindow.configure(background='blue')
        self.setupWindow.resizable(0, 0)

        # creating the userName variable, its descriptive label, entry field, and relevant error message label
        self.userName = tk.StringVar()
        self.userNameLabel = tk.Label(self.setupWindow, text="Please input your username, no special characters.", width=60, height=3).grid(row=0)
        self.userNameEntry = tk.Entry(self.setupWindow, textvariable=self.userName, width=20).grid(row=1)
        self.userNameButton = tk.Button(self.setupWindow, text="Submit", width=20, height=2, command=self.checkUsername).grid(row=2)
        self.userNameError = tk.Label(self.setupWindow, text="Invalid username. All characters must be alphanumeric. Try again.", width=60, height=3)

        # initializing the socket and relevant host and port variables
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = tk.StringVar()
        self.port = tk.IntVar()

        # creating widgets for providing host and port info, create the button for submitting that info
        self.hostLabel = tk.Label(self.setupWindow, text="Please enter the hostname or IP address of player 2.", width=60, height=3)
        self.hostEntry = tk.Entry(self.setupWindow, textvariable=self.host, width=20)
        self.portLabel = tk.Label(self.setupWindow, text="Please enter the port number that you want to connect through.", width=60, height=3)
        self.portEntry = tk.Entry(self.setupWindow, textvariable=self.port, width=20)
        self.hostPortButton = tk.Button(self.setupWindow, text="Submit", width=20, height=2, command=self.tryConnection)

        # creating widgets to display error messages
        self.portIntErrorLabel = tk.Label(self.setupWindow, text="Port must be an integer. Please try again.", width=60, height=3)
        self.invalidErrorLabel = tk.Label(self.setupWindow, text="Invalid host or port. Please try again.", width=60, height=3)
        self.waitForConnLabel = tk.Label(self.setupWindow, text="Waiting for connection...", width=60, height=3)

        self.setupWindow.mainloop()

    def checkUsername(self, event = None) -> None:
        """Determine if the entered userName is alphanumeric.

        Event: triggered upon clicking the userNameButton

        If the userName is valid, then the window rearranges widgets for providing host and port info.
        If not, the window displays the userName error messsage.
        """
        if self.userName.get().isalnum():
            self.hostLabel.grid(row=0)
            self.hostEntry.grid(row=1)
            self.portLabel.grid(row=2)
            self.portEntry.grid(row=3)
            self.hostPortButton.grid(row=4)
        else:
            self.userNameError.grid(row=0)

    def tryConnection(self, event = None) -> None:
        """Make use of the entered port and host info to establish a socket connection and initiate username exchange.

        Event: triggered upon clicking the hostPortButton

        If a non-integer is passed for the port number, an error message is displayed.
        If other invalid input or connection errors occur, the user is prompted whether to retry connecting.
        """
        try:
            portInt = int(self.port.get())

            if self.host.get() == "":
                raise ValueError
            
            self.s.bind((self.host.get(), portInt))
            self.s.listen(1)

            # removes error messages and puts up message clarifying the program is awaiting a connection
            self.invalidErrorLabel.grid_forget()
            self.portIntErrorLabel.grid_forget()
            self.hostPortButton.grid_forget()
            self.waitForConnLabel.grid(row=5)
            self.setupWindow.update()
            
            self.conn, self.addr = self.s.accept()
            self.exchangeUsernames()
        except tk.TclError:
            # tk.TclError is raised in place of a ValueError during port int conversion
            self.invalidErrorLabel.grid_forget()
            self.portIntErrorLabel.grid(row=5)
        except Exception:
            # covers for invalid hosts, os errors, and unusable ports
            self.portIntErrorLabel.grid_forget()
            self.invalidErrorLabel.grid(row=5)

    def exchangeUsernames(self) -> None:
        """Receive player1's username, create BoardClass type playerBoard, send userName, and intialize game.
        """
        player1Name = self.conn.recv(1024).decode()
        self.playerBoard = BoardClass(player1Name, self.userName.get())
        self.conn.sendall(self.userName.get().encode())
        self.createGameWindow()
        
    def createGameWindow(self) -> None:
        """Remove setupWindow, create and configure the root (game) window and relevant widgets.
        """
        self.setupWindow.destroy()
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe (Player 2)")
        self.root.geometry('378x450+550+50')
        self.root.configure(background='black')
        self.root.resizable(0, 0)
        self.setupGame()

    def createTileVariables(self) -> None:
        """Intialize variables to store the values of each gameboard tile.
        """
        self.tile1Value = tk.StringVar()
        self.tile2Value = tk.StringVar()
        self.tile3Value = tk.StringVar()
        self.tile4Value = tk.StringVar()
        self.tile5Value = tk.StringVar()
        self.tile6Value = tk.StringVar()
        self.tile7Value = tk.StringVar()
        self.tile8Value = tk.StringVar()
        self.tile9Value = tk.StringVar()

    def addBoardBorders(self) -> None:
        """Add black borders within the window for visual separation of gameboard tiles.
        """
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=1, column=1)
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=1, column=3)
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=3, column=1)
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=3, column=3)
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=5, column=1)
        tk.Label(self.root, bg="black", width=2, height=5).grid(row=5, column=3)
        tk.Label(self.root, bg="black", width=50, height=1).grid(row=2, columnspan=5)
        tk.Label(self.root, bg="black", width=50, height=1).grid(row=4, columnspan=5)

    def setupBoard(self) -> None:
        """Setup the visual gameboard by creating a label and button for each of the 9 tiles on the board.
        """
        # Tile 1
        self.tile1Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile1Value).grid(row=1, column=0)
        self.tile1Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileOne)
        self.tile1Button.grid(row=1, column=0)
        # Tile 2
        self.tile2Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile2Value).grid(row=1, column=2)
        self.tile2Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileTwo)
        self.tile2Button.grid(row=1, column=2)
        # Tile 3
        self.tile3Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile3Value).grid(row=1, column=4)
        self.tile3Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileThree)
        self.tile3Button.grid(row=1, column=4)
        # Tile 4
        self.tile4Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile4Value).grid(row=3, column=0)
        self.tile4Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileFour)
        self.tile4Button.grid(row=3, column=0)
        # Tile 5
        self.tile5Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile5Value).grid(row=3, column=2)
        self.tile5Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileFive)
        self.tile5Button.grid(row=3, column=2)
        # Tile 6
        self.tile6Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile6Value).grid(row=3, column=4)
        self.tile6Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileSix)
        self.tile6Button.grid(row=3, column=4)
        # Tile 7
        self.tile7Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile7Value).grid(row=5, column=0)
        self.tile7Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileSeven)
        self.tile7Button.grid(row=5, column=0)
        # Tile 8
        self.tile8Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile8Value).grid(row=5, column=2)
        self.tile8Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileEight)
        self.tile8Button.grid(row=5, column=2)
        # Tile 9
        self.tile9Label = tk.Label(self.root, width=15, height=5, textvariable = self.tile9Value).grid(row=5, column=4)
        self.tile9Button = tk.Button(self.root, width=15, height=5, bd=0, command=self.playTileNine)
        self.tile9Button.grid(row=5, column=4)

        self.addBoardBorders()

    def setupGame(self) -> None:
        """Setup the game by adding playerTurnLabel, initializing variables and gameboard, then starting mainloop.
        """
        # display of the current player's turn at the top of the game screen
        self.playerTurn = tk.StringVar()
        self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
        self.playerTurnLabel = tk.Label(self.root, textvariable = self.playerTurn, bg="green", width=49, height=3).grid(row=0, column=0, columnspan=5)

        # creation of visual board and setting canMove attribute
        self.createTileVariables()
        self.setupBoard()
        self.canMove = False

        # label that indicates program is waiting for player1 to indicate if a new game should be played
        self.playAgainLabel = tk.Label(self.root, width=49, height=3, bg="purple", text=f"Waiting for {self.playerBoard.getPlayer1Name()}")

        # After mainloop is initiated, the window calls otherPlayerTurn() to start off on player1's turn
        self.root.after(500, self.otherPlayerTurn)
        self.root.mainloop()

    def playTileOne(self, event = None) -> None:
        """Play out a player2 turn on tile one if player2 is allowed to make a move.

        Event: triggered by clicking on tile1Button

        Updates the gameboard with an O on tile one, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(1, "O")
            self.tile1Value.set(self.playerBoard.getGameBoardTile(1))
            self.tile1Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("1".encode())
            self.checkBoardCondition()

    def playTileTwo(self, event = None) -> None:
        """Play out a player2 turn on tile two if player2 is allowed to make a move.

        Event: triggered by clicking on tile2Button

        Updates the gameboard with an O on tile two, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(2, "O")
            self.tile2Value.set(self.playerBoard.getGameBoardTile(2))
            self.tile2Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("2".encode())
            self.checkBoardCondition()

    def playTileThree(self, event = None) -> None:
        """Play out a player2 turn on tile three if player2 is allowed to make a move.

        Event: triggered by clicking on tile3Button

        Updates the gameboard with an O on tile three, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(3, "O")
            self.tile3Value.set(self.playerBoard.getGameBoardTile(3))
            self.tile3Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("3".encode())
            self.checkBoardCondition()

    def playTileFour(self, event = None) -> None:
        """Play out a player2 turn on tile four if player2 is allowed to make a move.

        Event: triggered by clicking on tile4Button

        Updates the gameboard with an O on tile four, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(4, "O")
            self.tile4Value.set(self.playerBoard.getGameBoardTile(4))
            self.tile4Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("4".encode())
            self.checkBoardCondition()

    def playTileFive(self, event = None) -> None:
        """Play out a player2 turn on tile five if player2 is allowed to make a move.

        Event: triggered by clicking on tile5Button

        Updates the gameboard with an O on tile five, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(5, "O")
            self.tile5Value.set(self.playerBoard.getGameBoardTile(5))
            self.tile5Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("5".encode())
            self.checkBoardCondition()

    def playTileSix(self, event = None) -> None:
        """Play out a player2 turn on tile six if player2 is allowed to make a move.

        Event: triggered by clicking on tile6Button

        Updates the gameboard with an O on tile six, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(6, "O")
            self.tile6Value.set(self.playerBoard.getGameBoardTile(6))
            self.tile6Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("6".encode())
            self.checkBoardCondition()

    def playTileSeven(self, event = None) -> None:
        """Play out a player2 turn on tile seven if player2 is allowed to make a move.

        Event: triggered by clicking on tile7Button

        Updates the gameboard with an O on tile seven, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(7, "O")
            self.tile7Value.set(self.playerBoard.getGameBoardTile(7))
            self.tile7Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("7".encode())
            self.checkBoardCondition()

    def playTileEight(self, event = None) -> None:
        """Play out a player2 turn on tile eight if player2 is allowed to make a move.

        Event: triggered by clicking on tile8Button

        Updates the gameboard with an O on tile eight, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(8, "O")
            self.tile8Value.set(self.playerBoard.getGameBoardTile(8))
            self.tile8Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("8".encode())
            self.checkBoardCondition()

    def playTileNine(self, event = None) -> None:
        """Play out a player2 turn on tile nine if player2 is allowed to make a move.

        Event: triggered by clicking on tile9Button

        Updates the gameboard with an O on tile nine, switches turns, sends the move to player1, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        if self.canMove:
            self.playerBoard.updateGameBoard(9, "O")
            self.tile9Value.set(self.playerBoard.getGameBoardTile(9))
            self.tile9Button.grid_forget()
            self.playerBoard.setLastPlayer(self.playerBoard.getPlayer2Name())
            self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")
            self.conn.sendall("9".encode())
            self.checkBoardCondition()

    def tileOnePlayed(self) -> None:
        """Play out player1's move on tile one after receiving player1's move.

        Updates the gameboard with an X on tile one, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(1, "X")
        self.tile1Value.set(self.playerBoard.getGameBoardTile(1))
        self.tile1Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileTwoPlayed(self) -> None:
        """Play out player1's move on tile two after receiving player1's move.

        Updates the gameboard with an X on tile two, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(2, "X")
        self.tile2Value.set(self.playerBoard.getGameBoardTile(2))
        self.tile2Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileThreePlayed(self) -> None:
        """Play out player1's move on tile three after receiving player1's move.

        Updates the gameboard with an X on tile three, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(3, "X")
        self.tile3Value.set(self.playerBoard.getGameBoardTile(3))
        self.tile3Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileFourPlayed(self) -> None:
        """Play out player1's move on tile four after receiving player1's move.

        Updates the gameboard with an X on tile four, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(4, "X")
        self.tile4Value.set(self.playerBoard.getGameBoardTile(4))
        self.tile4Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileFivePlayed(self) -> None:
        """Play out player1's move on tile five after receiving player1's move.

        Updates the gameboard with an X on tile five, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(5, "X")
        self.tile5Value.set(self.playerBoard.getGameBoardTile(5))
        self.tile5Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileSixPlayed(self) -> None:
        """Play out player1's move on tile six after receiving player1's move.

        Updates the gameboard with an X on tile six, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(6, "X")
        self.tile6Value.set(self.playerBoard.getGameBoardTile(6))
        self.tile6Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileSevenPlayed(self) -> None:
        """Play out player1's move on tile seven after receiving player1's move.

        Updates the gameboard with an X on tile seven, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(7, "X")
        self.tile7Value.set(self.playerBoard.getGameBoardTile(7))
        self.tile7Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileEightPlayed(self) -> None:
        """Play out player1's move on tile eight after receiving player1's move.

        Updates the gameboard with an X on tile eight, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(8, "X")
        self.tile8Value.set(self.playerBoard.getGameBoardTile(8))
        self.tile8Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def tileNinePlayed(self) -> None:
        """Play out player1's move on tile nine after receiving player1's move.

        Updates the gameboard with an X on tile nine, switch to player2's turn, and
        finally runs a check if the game has ended upon completion of the turn.
        """
        self.playerBoard.updateGameBoard(9, "X")
        self.tile9Value.set(self.playerBoard.getGameBoardTile(9))
        self.tile9Button.grid_forget()
        self.playerBoard.setLastPlayer(self.playerBoard.getPlayer1Name())
        self.playerTurn.set(f"{self.playerBoard.getPlayer2Name()}'s Turn")
        self.checkBoardCondition()

    def checkBoardCondition(self) -> None:
        """Check if a game has ended, either by a win or a tie, and responds to that condition.

        Runs the BoardClass isWinner function, and if false, runs the BoardClass boardIsFull function to check
        for a win or tie. If the game is over, program awaits player1 message to start a new game or end the program.
        If the game is not over, then triggers the other player's turn function if it was just this player's turn.
        """
        self.root.update()
        
        if self.playerBoard.isWinner("O") or self.playerBoard.boardIsFull():
            # clearing buttons from the board to prevent interaction
            self.tile1Button.grid_forget()
            self.tile2Button.grid_forget()
            self.tile3Button.grid_forget()
            self.tile4Button.grid_forget()
            self.tile5Button.grid_forget()
            self.tile6Button.grid_forget()
            self.tile7Button.grid_forget()
            self.tile8Button.grid_forget()
            self.tile9Button.grid_forget()

            self.playAgainLabel.grid(row=6, columnspan=5)
            self.root.update()
            player1Response = self.conn.recv(1024).decode()

            if player1Response == "Play Again":
                self.newGame()
            elif player1Response == "Fun Times":
                self.endGame()
        else:
            if self.playerBoard.getPlayer2Name() == self.playerBoard.getLastPlayer():
                self.otherPlayerTurn()

    def otherPlayerTurn(self) -> None:
        """Play out the other player's turn first by receiving their move and applying that move to the relevant tile.
        """
        # prevents player2 from making a move during the other player's turn
        self.canMove = False
        player1Move = int(self.conn.recv(1024).decode())
        
        if player1Move == 1:
            self.tileOnePlayed()
        elif player1Move == 2:
            self.tileTwoPlayed()
        elif player1Move == 3:
            self.tileThreePlayed()
        elif player1Move == 4:
            self.tileFourPlayed()
        elif player1Move == 5:
            self.tileFivePlayed()
        elif player1Move == 6:
            self.tileSixPlayed()
        elif player1Move == 7:
            self.tileSevenPlayed()
        elif player1Move == 8:
            self.tileEightPlayed()
        elif player1Move == 9:
            self.tileNinePlayed()

        # upon completion of the other player's turn, player1 can make a move again
        self.canMove = True
    
    def newGame(self) -> None:
        """Begin a new game by resetting the gameboard both internally and visually, starts on player1's turn.
        """
        self.playAgainLabel.grid_forget()
        # resets the internal BoardClass gameboard
        self.playerBoard.resetGameBoard()
        self.playerTurn.set(f"{self.playerBoard.getPlayer1Name()}'s Turn")

        # readd the buttons for interaction
        self.tile1Button.grid(row=1, column=0)
        self.tile2Button.grid(row=1, column=2)
        self.tile3Button.grid(row=1, column=4)
        self.tile4Button.grid(row=3, column=0)
        self.tile5Button.grid(row=3, column=2)
        self.tile6Button.grid(row=3, column=4)
        self.tile7Button.grid(row=5, column=0)
        self.tile8Button.grid(row=5, column=2)
        self.tile9Button.grid(row=5, column=4)

        # resetting visual gameboard values
        self.tile1Value.set("")
        self.tile2Value.set("")
        self.tile3Value.set("")
        self.tile4Value.set("")
        self.tile5Value.set("")
        self.tile6Value.set("")
        self.tile7Value.set("")
        self.tile8Value.set("")
        self.tile9Value.set("")

        # new game starts on player1 turn so otherPlayerTurn() must be called
        self.root.update()
        self.otherPlayerTurn()

    def endGame(self) -> None:
        """End the program by clearing extra widgets, closing the socket, and displaying final statistics.
        """
        self.playAgainLabel.grid_forget()
        self.conn.sendall("Closing".encode())
        self.conn.close()
        self.displayStats()

    def displayStats(self) -> None:
        """Display the final stats returned from internal BoardClass computeStats() method, and quit the mainloop.
        """
        self.finalStats = tk.StringVar()
        self.finalStats.set(self.playerBoard.computeStats())
        self.statsLabel = tk.Label(self.root, textvariable=self.finalStats, bg="pink", width=49, height=7)
        self.statsLabel.grid(row=6, columnspan=5)
        self.root.quit()

if __name__ == "__main__":
    ticTacToeGame = player2UI()
