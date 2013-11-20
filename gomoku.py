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
        self.player_x = Player('X')
        self.player_o = Player('O')
        self.max_depth = int(dimension/2)
        self.minimax_val = 0

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
        elif i == 2:
            self.minimax_val = 1
            self.initial = self.player_o
            self.oponent = self.player_x
        else:
            print("Only Two Players Available")
            sys.exit()

        self.current = self.initial
        while self.isOver() is not True:
            initial = self.current

            if initial.piece == 'X':
                best, heuristic = self.alphaBetaSearch(initial,
                                                       self.max_depth)
                self.state = self.state.createNewState(best, initial)
                self.printCurrentBoard()
                if heuristic is not None:
                    print("Best Move: %s" % (best,))
                    print("Heuristic Value: %d" % heuristic)
                    print("------------------------------------------", end='\n')
                else:
                    print("No Move Found.")
                    print("(-1, -1)")
                    print("------------------------------------------", end='\n')
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
        elif i == 2:
            self.initial = self.player_o
            self.oponent = self.player_x
        else:
            print("Only Two Players Available")
            sys.exit()

        self.current = self.initial
        while self.isOver() is not True:
            initial = self.current
            if self.initial == initial:
                self.minimax_val = 2
            else:
                self.minimax_val = 1
            best, heuristic = self.alphaBetaSearch(self.current,
                                                   self.max_depth)
            self.state = self.state.createNewState(best, initial)
            self.printCurrentBoard()

            if self.state.isWinner(initial, self.chain) is True:
                self.winner = initial

            self.current = self.swapTurn(initial)

            if heuristic is not None:
                print("Best Move: %s" % (best,))
                print("Heuristic Value: %d" % heuristic)
                print("------------------------------------------", end='\n')
                input("Press Enter..")
            else:
                print("No Move Found.")
                print("(-1, -1)")
                print("------------------------------------------", end='\n')

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
        max_valid = None
        max_utility = None
        alpha = None
        beta = None

        valid = self.state.getValidTransitions(player)
        for move, state in valid:
            utility = self.minValue(state, self.swapInitial(player),
                                    alpha, beta, depth-1)

            if max_utility is None or utility > max_utility:
                max_valid = move
                max_utility = utility

            if beta is not None and utility >= beta:
                return move

            if alpha is None or utility > alpha:
                alpha = utility

        return max_valid, max_utility

    def minValue(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self, self.swapInitial(player))
        else:
            valid = state.getValidTransitions(player)
            min_utility = None
            for move, state in valid:
                utility = self.maxValue(state, self.swapInitial(player),
                                        alpha, beta, depth-1)
                if min_utility is None or utility < min_utility:
                    min_utility = utility

                if alpha is not None and utility <= alpha:
                    return utility

                if beta is None or utility < beta:
                    beta = utility
            return min_utility

    def maxValue(self, state, player, alpha, beta, depth):
        if depth == 0:
            return state.heuristic(self, self.swapInitial(player))
        else:
            valid = state.getValidTransitions(player)
            max_utility = None
            for move, state in valid:
                utility = self.minValue(state, self.swapInitial(player),
                                        alpha, beta, depth-1)
                if max_utility is None or utility > max_utility:
                    max_utility = utility

                if beta is not None and utility >= beta:
                    return utility

                if alpha is None or utility > alpha:
                    alpha = utility
            return max_utility
