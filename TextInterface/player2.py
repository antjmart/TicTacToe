# SERVER
from gameboard import InvalidMove
from gameboard import BoardClass
import socket

def establishConnection(s: socket) -> socket:
    """Establishes a socket with a user input host and port, then waits for and accepts a connection on the socket.

    s: A socket type object that uses the user input host and port to establish a socket connection.

    Returns:
        conn: socket type object representing the connection the server just made over the socket.
    """
    while True:
        try:
            host = input("Please enter the hostname or IP address to establish a connection for.\n").lower()
            port = int(input("Please enter the port number that you want to connect through.\n"))
            s.bind((host, port))
            s.listen(1)
            break
        except ValueError:
            print("Port must be an integer. Please try again.")
        except Exception:
            print("Invalid host or port. Please try again.")
    
    print("Waiting for connection...")
    conn, addr = s.accept()
    return conn
    
def exchangeUsernames(conn: socket, playerBoard: BoardClass) -> None:
    """Receives player1's username over the socket, sets the otherPlayer attribute, then sends "player2" over the socket.

    conn: socket type object representing the socket connection with player1.
    playerBoard: BoardClass type object that stores all of the game information for player2.
    """
    player1Name = conn.recv(1024).decode()
    playerBoard.setOtherPlayer(player1Name)
    conn.sendall("player2".encode())

def beginGame(playerBoard: BoardClass) -> None:
    """Begins a game by outputing the game instructions and a fresh game board without moves.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    """
    playerBoard.printInstructions()
    print("Start Game.")
    playerBoard.printBoard()

def takeTurn(playerBoard: BoardClass, conn: socket) -> None:
    """Plays out an entire turn for player2.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    conn: socket type object representing the socket connection with player1.

    User inputs what move they want to make. If valid, the board is updated, printed out,
    and the move is sent to player1 over the socket.
    """
    while True:
        try:
            player2Move = int(input("Enter your move (number from 1 - 9): "))
        
            if not 1 <= player2Move <= 9:
                raise ValueError

            playerBoard.updateGameBoard(player2Move, "O")
            break
        except ValueError:
            # Triggered when the move input is a non-integer or invalid integer.
            print("Invalid input. Please try again.")
        except InvalidMove:
            # Custom exception triggered when a game piece is already placed on input tile.
            print("That tile has already been played. Please try again.")

    playerBoard.printBoard()
    conn.sendall(str(player2Move).encode())
    # For this and future uses, upkeeps the lastPlayer attribute after a move is made.
    playerBoard.setLastPlayer(playerBoard.getPlayerName())

def otherPlayerTurn(playerBoard: BoardClass, conn: socket) -> None:
    """Plays out an entire turn for player1.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    conn: socket type object representing the socket connection with player1.

    Receives player1's move over the socket, updates gameboard with their move, outputs updated board.
    """
    # Output to terminal while waiting for player1 to make their move.
    print(f"{playerBoard.getOtherPlayer()}'s Turn...")
    player1Move = int(conn.recv(1024).decode())
    playerBoard.updateGameBoard(player1Move, "X")
    playerBoard.printBoard()
    playerBoard.setLastPlayer(playerBoard.getOtherPlayer())

def determineBoardCondition(playerBoard: BoardClass, conn: socket) -> str:
    """Determines the condition of the board and how to respond.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    conn: socket type object representing the socket connection with player1.

    If there is no winner or tie, play continues. If a game-ending event occurs, waits
    for input from player1 over the socket to determine if a new game should be played,
    or if the games should be ended.
    """
    if playerBoard.isWinner("O") or playerBoard.boardIsFull():
        print(f"Waiting for {playerBoard.getOtherPlayer()}...")
        player1Response = conn.recv(1024).decode()

        if player1Response == "Play Again":
            return "New Game"
        elif player1Response == "Fun Times":
            return "End Game"
    else:
        # "Continue" is a filler return value when "New Game" and "End Game" do not apply
        return "Continue"

def newGame(playerBoard: BoardClass) -> None:
    """Establishes a new game by clearing the gameboard and beginning a game.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    """
    playerBoard.resetGameBoard()
    beginGame(playerBoard)

def endGame(conn: socket) -> None:
    """Ends the game by closing the connection, notifies player1 over the connection before closing.

    conn: socket type object representing the socket connection with player1.
    """
    print("Closing connection.\n")
    conn.sendall("Closing".encode())
    conn.close()

def playGames(playerBoard: BoardClass, conn: socket) -> None:
    """Plays out a series of games until player1 decides to stop playing.

    playerBoard: BoardClass type object that stores all of the game information for player2.
    conn: socket type object representing the socket connection with player1.

    Loops through player1 taking their turn, checking if game-ending condition occurred,
    player2 taking their turn, then checking again if game-ending condition occurred. When a
    game-ending condition occurs, either starts a new game, or ends the game/program altogether.
    """
    while True:
        otherPlayerTurn(playerBoard, conn)
        boardCondition = determineBoardCondition(playerBoard, conn)

        if boardCondition == "New Game":
            # New game is started, restarts loop so that player1 (the other player) has first turn.
            newGame(playerBoard)
            continue
        elif boardCondition == "End Game":
            # Games are fully ended by breaking out of this function loop.
            endGame(conn)
            break

        takeTurn(playerBoard, conn)
        boardCondition = determineBoardCondition(playerBoard, conn)

        if boardCondition == "New Game":
            newGame(playerBoard)
        elif boardCondition == "End Game":
            endGame(conn)
            break

def main() -> None:
    """Main function for running the program.

    A socket object is created, user inputs a username, a BoardClass object is created to hold
    player2's information, a socket connection is established, games are played out, and in
    the end final stats for player2 are printed out.
    """
    # playerBoard becomes player2's BoardClass object
    playerBoard = BoardClass("player2")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # conn must be used instead of the socket s, as the server
    conn = establishConnection(s)
    exchangeUsernames(conn, playerBoard)

    beginGame(playerBoard)
    playGames(playerBoard, conn)
    # Printing stats is last step before ending the program
    playerBoard.printStats()


if __name__ == "__main__":
    main()
