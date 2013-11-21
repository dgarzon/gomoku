import sys
from state import *
from player import *
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")


class Gomoku(object):
    def __init__(self, dimension, chain, limit):
        super(Gomoku, self).__init__()
        self.state = State()
        self.dimension = dimension
        self.chain = chain
        self.limit = limit
        self.winner = None
        self.initial = None
        self.current = None
        self.oponent = None
        self.player_x = Player('X')
        self.player_o = Player('O')
        self.max_depth = int(dimension/2)
        self.minimax_moves = []

    def start(self):
        self.state.board.initializeBoard(self.dimension)
        if self.mode == 1:
            self.manualGame()
        elif self.mode == 2:
            self.agentTournamentGame()
        elif self.mode == 3:
            self.agentVsAgentGame()

    def swapTurn(self, player):
        if player == self.player_x:
            self.current = self.player_o
            self.oponent = self.player_x
            return self.player_o
        else:
            self.current = self.player_x
            self.oponent = self.player_o
            return self.player_x

    def swapInitial(self, player):
        if player == self.player_x:
            return self.player_o
        else:
            return self.player_x

    def manualGame(self):
        print("Start:                                    ", end='\n')
        print(" 1. Human (X)                             ", end='\n')
        print(" 2. Human (O)                             ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.initial = self.player_x
            self.oponent = self.player_o
        elif i == 2:
            self.initial = self.player_o
            self.oponent = self.player_x
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
            self.state = self.state.createNewState(move, self.current)
            if self.state.isWinner(self.current, self.chain) is True:
                self.winner = self.current
            self.current = self.swapTurn(self.current)

        if self.winner is not None:
            self.printWinMessage()
        else:
            self.printGameEnded()
            self.state.board.printBoard()
            print("------------------------------------------", end='\n')
            print("                 Tie                      ", end='\n')
            print("------------------------------------------", end='\n')

    def getMaxMove(self):
        max_move = max(self.minimax_moves, key=lambda item: item[0])[1]
        print(max_move)
        return max_move

    def randomGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Machine (X)                             ", end='\n')
        print(" 2. Random (O)                              ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.current = self.player_x
            self.oponent = self.player_o
        elif i == 2:
            self.current = self.player_o
            self.oponent = self.player_x
        else:
            print("Only Two Players Available")
            sys.exit()

        while self.isOver() is not True:
            print("In loop..")

    def agentTournamentGame(self):
        print("Start:                                         ", end='\n')
        print(" 1. My Agent Starts (X)                        ", end='\n')
        print(" 2. Other Agent Starts (O)                     ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.minimax_val = 2
            self.initial = self.player_x
            self.oponent = self.player_o
            rand = self.state.board.randomMove()
            self.state = self.state.createNewState(rand, self.initial)
            self.printCurrentBoard()
            print("Initial Move: %s" % (rand,))
            print("------------------------------------------", end='\n')
            self.current = self.oponent
        elif i == 2:
            self.minimax_val = 1
            self.initial = self.player_o
            self.oponent = self.player_x
            self.current = self.initial
        else:
            print("Only Two Players Available")
            sys.exit()

        while self.isOver() is not True:
            initial = self.current

            if initial.piece == 'X':
                heuristic = None
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(self.limit)
                try:
                    heuristic = self.alphaBetaSearch(initial,
                                                     self.max_depth)
                except Exception:
                    self.state = self.state.createNewState(self.state.board.closeMove(self.state.move), initial)
                    self.printCurrentBoard()
                    print("Best Move: %s" % (self.state.move,))
                    print("------------------------------------------", end='\n')
                    self.minimax_moves = []

                if heuristic is not None:
                    best = self.getMaxMove()
                    self.state = self.state.createNewState(best, initial)
                    self.printCurrentBoard()
                    print("Best Move: %s" % (best,))
                    print("Heuristic Value: %d" % heuristic)
                    print("------------------------------------------", end='\n')
                    self.minimax_moves = []

            else:
                flag = True
                while flag is True:
                    move = initial.getMove()
                    if self.state.board.isValidMove(move):
                        flag = None
                    else:
                        print("Spot Taken.")
                self.state = self.state.createNewState(move, initial)
                self.printCurrentBoard()

            if self.state.isWinner(initial, self.chain) is True:
                self.winner = initial

            self.current = self.swapTurn(initial)

        if self.winner is not None:
            self.printWinMessage()
        else:
            self.printGameEnded()
            self.state.board.printBoard()
            print("------------------------------------------", end='\n')
            print("                 Tie                      ", end='\n')
            print("------------------------------------------", end='\n')

    def printCurrentBoard(self):
        print("------------------------------------------", end='\n')
        print("              Current Board               ")
        print("------------------------------------------", end='\n')
        self.state.board.printBoard()
        print("------------------------------------------", end='\n')

    def agentVsAgentGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Agent (X)                             ", end='\n')
        print(" 2. Agent (O)                             ", end='\n')

        i = int(input("Choose Starting Player: "))
        if i == 1:
            self.initial = self.player_x
            self.oponent = self.player_o
            rand = self.state.board.randomMove()
            self.state = self.state.createNewState(rand, self.initial)
            self.printCurrentBoard()
            print("Initial Move: %s" % (rand,))
            print("------------------------------------------", end='\n')
            self.current = self.oponent
        elif i == 2:
            self.initial = self.player_o
            self.oponent = self.player_x
            self.current = self.initial
        else:
            print("Only Two Players Available")
            sys.exit()

        while self.isOver() is not True:
            initial = self.current
            heuristic = None
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(self.limit)
            try:
                heuristic = self.alphaBetaSearch(self.current,
                                                 self.max_depth)
                best = self.getMaxMove()
                self.state = self.state.createNewState(best, initial)
                self.printCurrentBoard()
                self.minimax_moves = []

                print("Best Move: %s" % (best,))
                print("Heuristic Value: %d" % heuristic)
                print("------------------------------------------", end='\n')
                input("Press Enter..")

            except Exception:
                self.state = self.state.createNewState(self.state.board.closeMove(self.state.move), initial)
                self.printCurrentBoard()
                print("Best Move: %s" % (self.state.move,))
                print("------------------------------------------", end='\n')
                self.minimax_moves = []

            if self.state.isWinner(initial, self.chain) is True:
                self.winner = initial

            self.current = self.swapTurn(initial)

        if self.winner is not None:
            self.printWinMessage()
        else:
            self.printGameEnded()
            self.state.board.printBoard()
            print("------------------------------------------", end='\n')
            print("                 Tie                      ", end='\n')
            print("------------------------------------------", end='\n')

    def displayMenu(self):
        print("------------------------------------------", end='\n')
        print("             Welcome to Gomoku            ", end='\n')
        print("------------------------------------------", end='\n')
        print("Modes:                                    ")
        print(" 1. Human vs. Human                       ")
        print(" 2. Tournament                            ")
        print(" 3. Agent vs. Agent                       ")
        print(" 4. Random vs. Agent                      ")
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

    def alphaBetaSearch(self, player, depth):
        alpha = float('-inf')
        beta = float('inf')

        valid = self.state.getValidTransitions(player)

        utility = self.maxValue(self.state, player,
                                alpha, beta, depth-1)

        return utility

    def minValue(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self, player)
        else:
            valid = state.getValidTransitions(player)
            utility = float('inf')
            for move, state in valid:
                utility = min(utility,
                              self.maxValue(state, self.swapInitial(player),
                                            alpha, beta, depth-1))
                if utility <= alpha:
                    return utility
                beta = min(beta, utility)

            return utility

    def maxValue(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self, player)
        else:
            valid = state.getValidTransitions(player)
            utility = float('-inf')
            for move, state in valid:
                utility = max(utility,
                              self.minValue(state, self.swapInitial(player),
                                            alpha, beta, depth-1))
                self.minimax_moves.append((utility, move))
                if utility >= beta:
                    return utility
                alpha = max(alpha, utility)

            return utility
