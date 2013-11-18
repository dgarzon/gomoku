from state import *
from player import *

class Gomoku(object):
    def __init__(self, dimension, chain, limit):
        super(Gomoku, self).__init__()
        self.state = State()
        self.dimension = dimension
        self.chain = chain
        self.limit = limit
        self.winner = None
        self.current = None
        self.player_x = Player('X', [])
        self.player_o = Player('O', [])
        self.mode = None

    def start(self):
        self.state.board.initializeBoard(self.dimension)
        if self.mode == 1:
            self.manualGame()

    def manualGame(self):
        print("Start:                                    ", end='\n')
        print(" 1. Human (X)                             ", end='\n')
        print(" 2. Human (O)                             ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.current = self.player_x
        elif i == 2:
            self.current = self.player_o
        else:
            print("Only Two Players Available")
            sys.exit()

        print("------------------------------------------", end='\n')
        print("               Start Board                ", end='\n')
        print("------------------------------------------", end='\n')
        while self.isOver() is not True:
            self.state.board.printBoard()
            print("------------------------------------------", end='\n')
            move = self.current.getMove()
            if self.state.board.isValidMove(move):
                self.state = self.createNewState(move)
                if self.isWinner(move, self.current):
                    self.winner = self.current
                self.swapTurn()
            else:
                print("Invalid Move, Try Again")

        if self.winner is not None:
            self.printWinMessage()
        else:
            self.printGameEnded()
            self.state.board.printBoard()
            print("------------------------------------------", end='\n')
            print("                 Tie                      ", end='\n')
            print("------------------------------------------", end='\n')

    def randomGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Machine (X)                             ", end='\n')
        print(" 2. Random (O)                              ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.current = self.player_x
        elif i == 2:
            self.current = self.player_o
        else:
            print("Only Two Players Available")
            sys.exit()

        while game.isOver() is not True:
            print("In loop..")

    def agentMachineGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Machine (X)                             ", end='\n')
        print(" 2. Machine (O)                              ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.current = self.player_x
        elif i == 2:
            self.current = self.player_o
        else:
            print("Only Two Players Available")
            sys.exit()

        while game.isOver() is not True:
            print("In loop..")

    def machineMachineGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Machine (X)                             ", end='\n')
        print(" 2. Machine (O)                              ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.current = self.player_x
        elif i == 2:
            self.current = self.player_o
        else:
            print("Only Two Players Available")
            sys.exit()

        while game.isOver() is not True:
            print("In loop..")

    def swapTurn(self):
        if self.current == self.player_x:
            self.current = self.player_o
        else:
            self.current = self.player_x

    def displayMenu(self):
        print("------------------------------------------", end='\n')
        print("             Welcome to Gomoku            ", end='\n')
        print("------------------------------------------", end='\n')
        print("Modes:                                    ")
        print(" 1. Human vs. Human                       ")
        print(" 2. Agent vs. Machine                     ")
        print(" 3. Random vs. Agent                      ")
        print(" 3. Agent vs. Agent                       ")
        print("------------------------------------------", end='\n')

    def printWinMessage(self):
        print("------------------------------------------", end='\n')
        self.state.board.printBoard()
        print("------------------------------------------", end='\n')
        print("            Player %s Wins                " % self.winner.piece)
        print("------------------------------------------", end='\n')

    def printGameEnded(self):
        print("------------------------------------------", end='\n')
        print("              Game Ended                  ")
        print("------------------------------------------", end='\n')

    def isOver(self):
        return self.winner is not None or\
            not self.state.board.getValidMoves()

    # http://stackoverflow.com/questions/2670217/detect-winning-game-in-nought-and-crosses
    def isWinner(self, move, player):
        count = 0
        # North
        for row in reversed(range(move[0])):
            if self.state.board.board[(row, move[1])] == player.piece:
                count += 1
            else:
                break

        # South
        for row in range(move[0], self.dimension):
            if self.state.board.board[(row, move[1])] == player.piece:
                count += 1
            else:
                break

        if count == self.chain:
            print("N/S")
            return True

        count = 0
        # East
        for col in range(move[1], self.dimension):
            if self.state.board.board[(move[0], col)] == player.piece:
                count += 1
            else:
                break

        # West
        for col in reversed(range(move[1])):
            if self.state.board.board[(move[0], col)] == player.piece:
                count += 1
            else:
                break

        if count == self.chain:
            print("E/W")
            return True

        count = 0
        # North West
        for row, col in zip(reversed(range(move[0])),
                            reversed(range(move[1]))):
            if self.state.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        # South East
        for row, col in zip(range(move[0], self.dimension),
                            range(move[1], self.dimension)):
            if self.state.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        if count == self.chain:
            print("NW/SE")
            return True

        count = 0
        # North East
        for row, col in zip(reversed(range(move[0])),
                            range(move[1] + 1, self.dimension)):
            if self.state.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        # South West
        for row, col in zip(range(move[0], self.dimension),
                            reversed(range(move[1] + 1))):
            if self.state.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        if count == self.chain:
            print("NE/SW")
            return True

        return False

    def createNewState(self, move):
        new_board = self.state.board
        new_board.makeMove(move, self.current)
        new_state = State()
        new_state.parent = self.state
        new_state.board = new_board

        return new_state
