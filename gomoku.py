import sys
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
        self.initial = None
        self.current = None
        self.oponent = None
        self.player_x = Player('X', [])
        self.player_o = Player('O', [])
        self.mode = None
        self.max_depth = int(dimension/2 - 1)

    def start(self):
        self.state.board.initializeBoard(self.dimension)
        if self.mode == 1:
            self.manualGame()
        elif self.mode == 2:
            self.agentTournamentGame()

    def swapTurn(self, player):
        if player == self.player_x:
            self.current = self.player_o
            return self.player_o
        else:
            self.current = self.player_x
            return self.player_x

    def manualGame(self):
        print("Start:                                    ", end='\n')
        print(" 1. Human (X)                             ", end='\n')
        print(" 2. Human (O)                             ", end='\n')

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
        print("Start:                                    ", end='\n')
        print(" 1. Agent (X)                             ", end='\n')
        print(" 2. Agent (O)                             ", end='\n')

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

        self.current = self.initial
        while self.isOver() is not True:
            initial = self.current

            if initial == self.initial:
                best = self.alpha_beta_search(self.current, self.max_depth)
                self.state = self.state.createNewState(best, initial)
                self.printCurrentBoard()
                print("Best Move: %s" % (best,))
                print("------------------------------------------", end='\n')
            else:
                move = initial.getMove()
                self.state = self.state.createNewState(move, initial)
                self.printCurrentBoard()

            if self.state.isWinner(initial, self.chain) is True:
                self.winner = initial
                self.printWinMessage()

            self.current = self.swapTurn(initial)

    def printCurrentBoard(self):
        print("------------------------------------------", end='\n')
        print("              Current Board               ")
        print("------------------------------------------", end='\n')
        self.state.board.printBoard()
        print("------------------------------------------", end='\n')

    def machineMachineGame(self):
        print("Start:                                      ", end='\n')
        print(" 1. Machine (X)                             ", end='\n')
        print(" 2. Machine (O)                             ", end='\n')

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

    def alpha_beta_search(self, player, depth):
        max_valid = None
        max_utility = None
        alpha = None
        beta = None

        valid = self.state.getValidTransitions(player)
        for move, state in valid:
            utility = self.min_value(state, self.swapTurn(player),
                                     alpha, beta, depth)

            if max_utility is None or utility > max_utility:
                max_valid = move
                max_utility = utility

            if beta is not None and utility >= beta:
                return move

            if alpha is None or utility > alpha:
                alpha = utility

        return max_valid

    def min_value(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self.initial, self.oponent, self.chain)
        else:
            valid = state.getValidTransitions(player)
            min_utility = None
            for move, state in valid:
                utility = self.max_value(state, self.swapTurn(player),
                                         alpha, beta, depth-1)
                if min_utility is None or utility < min_utility:
                    min_utility = utility

                if alpha is not None and utility <= alpha:
                    return utility

                if beta is None or utility < beta:
                    beta = utility
            return min_utility

    def max_value(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self.initial, self.oponent, self.chain)
        else:
            valid = state.getValidTransitions(player)
            max_utility = None
            for move, state in valid:
                utility = self.min_value(state, self.swapTurn(player),
                                         alpha, beta, depth-1)
                if max_utility is None or utility > max_utility:
                    max_utility = utility

                if beta is not None and utility >= beta:
                    return utility

                if alpha is None or utility > alpha:
                    alpha = utility
            return max_utility
