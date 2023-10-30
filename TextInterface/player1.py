# CLIENT
from gameboard import InvalidMove
from gameboard import BoardClass
import socket

def establishConnection(s: socket) -> None:
    """Takes in a user input host and port, then attempts to make a connection with those over the socket.

    s: A socket type object that uses the user input host and port to establish a socket connection.
    """
    host = input("Please enter the hostname or IP address of player 2.\n").lower()
    port = int(input("Please enter the port number that you want to connect through.\n"))
    s.connect((host, port))

def exchangeUsernames(s: socket, playerBoard: BoardClass) -> None:
    """Sends username to player2, receives player2's username, sets otherPlayer attribute.

    s: socket type object representing the socket connection with player2.
    playerBoard: BoardClass type object that stores all of the game information for player1.
    """
    s.sendall(playerBoard.getPlayerName().encode())
    player2Name = s.recv(1024).decode()
    playerBoard.setOtherPlayer(player2Name)

def beginGame(playerBoard: BoardClass) -> None:
    """Begins a game by outputing the game instructions and a fresh game board without moves.

    playerBoard: BoardClass type object that stores all of the game information for player1.
    """
    playerBoard.printInstructions()
    print("Start Game.")
    playerBoard.printBoard()

def takeTurn(playerBoard: BoardClass, s: socket) -> None:
    """Plays out an entire turn for player1.

    playerBoard: BoardClass type object that stores all of the game information for player1.
    s: socket type object representing the socket connection with player2.

    User inputs what move they want to make. If valid, the board is updated, printed out,
    and the move is sent to player2 over the socket.
    """
    while True:
        try:
            player1Move = int(input("Enter your move (number from 1 - 9): "))
        
            if not 1 <= player1Move <= 9:
                raise ValueError

            playerBoard.updateGameBoard(player1Move, "X")
            break
        except ValueError:
            # Triggered when the move input is a non-integer or invalid integer.
            print("Invalid input. Please try again.")
        except InvalidMove:
            # Custom exception triggered when a game piece is already placed on input tile.
            print("That tile has already been played. Please try again.")
        
    playerBoard.printBoard()
    s.sendall(str(player1Move).encode())
    # For this and future uses, upkeeps the lastPlayer attribute after a move is made.
    playerBoard.setLastPlayer(playerBoard.getPlayerName())

def otherPlayerTurn(playerBoard: BoardClass, s: socket) -> None:
    """Plays out an entire turn for player2.

    playerBoard: BoardClass type object that stores all of the game information for player1.
    s: socket type object representing the socket connection with player2.

    Receives player2's move over the socket, updates gameboard with their move, outputs updated board.
    """
    # Output to terminal while waiting for player2 to make their move.
    print(f"{playerBoard.getOtherPlayer()}'s Turn...")
    player2Move = int(s.recv(1024).decode())
    playerBoard.updateGameBoard(player2Move, "O")
    playerBoard.printBoard()
    playerBoard.setLastPlayer(playerBoard.getOtherPlayer())

def determineBoardCondition(playerBoard: BoardClass) -> str:
    """Determines the condition of the board and how to respond.

    playerBoard: BoardClass type object that stores all of the game information for player1.

    If there is no winner or tie, play continues. If a game-ending event occurs, user inputs
    whether they want to play again. If so, determines for a new game to be played, determines
    to end the games if not.
    """
    if playerBoard.isWinner("X") or playerBoard.boardIsFull():
        playAgain = input("Do you want to play again? (y/n)\n").lower()

        while playAgain != "y" and playAgain != "n":
            playAgain = input("Invalid input. Please enter y or n.\n").lower()

        if playAgain == "y":
            return "New Game"
        elif playAgain == "n":
            return "End Game"
    else:
        # "Continue" is a filler return value when "New Game" and "End Game" do not apply
        return "Continue"

def newGame(playerBoard: BoardClass, s: socket) -> None:
    """Establishes a new game by clearing the gameboard and beginning a game, messages player2 to play again.

    playerBoard: BoardClass type object that stores all of the game information for player1.
    """
    s.sendall("Play Again".encode())
    playerBoard.resetGameBoard()
    beginGame(playerBoard)

def endGame(s: socket) -> None:
    """Sends 'fun times' over the socket to signify ending the game, closes socket upon player2 confirmation.

    s: socket type object representing the socket connection with player2.
    """
    s.sendall("Fun Times".encode())
    # Waits for message from player2 to make sure the server connection is closed before the socket.
    waitToClose = s.recv(1024).decode()
    print("Closing socket.\n")
    s.close()

def playGames(playerBoard: BoardClass, s: socket) -> None:
    """Plays out a series of games until the user decides to stop playing.

    playerBoard: BoardClass type object that stores all of the game information for player1.
    s: socket type object representing the socket connection with player2.

    Loops through player1 taking their turn, checking if game-ending condition occurred,
    player2 taking their turn, then checking again if game-ending condition occurred. When a
    game-ending condition occurs, either starts a new game, or ends the game/program altogether.
    """
    while True:
        takeTurn(playerBoard, s)
        boardCondition = determineBoardCondition(playerBoard)
        
        if boardCondition == "New Game":
            # New game is started, restarts loop so that player1 has first turn.
            newGame(playerBoard, s)
            continue
        elif boardCondition == "End Game":
            # Games are fully ended by breaking out of this function loop.
            endGame(s)
            break
        
        otherPlayerTurn(playerBoard, s)
        boardCondition = determineBoardCondition(playerBoard)

        if boardCondition == "New Game":
            newGame(playerBoard, s)
        elif boardCondition == "End Game":
            endGame(s)
            break

def retryConnection() -> bool:
    """Determines if user wants to retry connecting to the server, takes user input.

    Returns:
        True if user inputs y or Y for yes.
        False if user inputs n or N for no.
    """
    retryConn = input("Do you want to try again? (y/n)\n").lower()
            
    while retryConn != "y" and retryConn != "n":
        retryConn = input("Invalid input. Please enter y or n.\n").lower()

    if retryConn == "n":
        return False

    # By default, retryConn is equal to "y" at this point
    return True

def main() -> None:
    """Main function for running the program.

    A socket object is created, user inputs a username, a BoardClass object is created to hold
    player1's information, a socket connection is established, games are played out, and in
    the end final stats for player1 are printed out.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    userName = input("Please input your username, no special characters.\n")

    # ensures the username is alphanumeric
    while not userName.isalnum():
        userName = input("Invalid username. All characters must be alphanumeric. Try again.\n")

    # playerBoard becomes player1's BoardClass object
    playerBoard = BoardClass(userName)
    
    while True:  
        try:
            establishConnection(s)
            exchangeUsernames(s, playerBoard)
            break
        except ValueError:
            print("Port must be an integer. Please try again.")
        except ConnectionError:
            # Triggers if valid host and port are given, but fails to make a connection, prompts for retry
            print("Connection failed.")
            if not retryConnection():
                # Blank return statement used to fully break out of the main function
                return
        except Exception:
            # Catches other exceptions, including OS errors, host format errors, invalid ports, prompts for retry
            print("Invalid host or port.")
            if not retryConnection():
                return

    beginGame(playerBoard)
    playGames(playerBoard, s)
    # Printing stats is last step before ending the program
    playerBoard.printStats()


if __name__ == "__main__":
    main()
