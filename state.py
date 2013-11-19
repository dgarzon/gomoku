import copy
from board import *


class State(object):
    def __init__(self):
        super(State, self).__init__()
        self.move = (0, 0)
        self.board = Board()
        self.parent = None

    def heuristic(self, player, oponent, chain):
        if self.isWinner(player, chain):
            return 1
        if self.isWinner(oponent, chain):
            return -1
        return 0

    def createNewState(self, move, player):
        new = State()
        new.board = copy.deepcopy(self.board)
        new.move = new.board.makeMove(move, player)
        new.player = player

        if new.move == (-1, -1):
            return None
        return new

    def getValidTransitions(self, player):
        valid = self.board.getValidMoves()
        transitions = []
        for move in valid:
            new_state = self.createNewState(move, player)
            transitions.append((move, new_state))

        return transitions

    def isWinner(self, player, chain):
        count = 0
        # North
        for row in reversed(range(self.move[0])):
            if self.board.board[(row, self.move[1])] == player.piece:
                count += 1
            else:
                break

        # South
        for row in range(self.move[0], self.board.dimension):
            if self.board.board[(row, self.move[1])] == player.piece:
                count += 1
            else:
                break

        if count == chain:
            return True

        count = 0
        # East
        for col in range(self.move[1], self.board.dimension):
            if self.board.board[(self.move[0], col)] == player.piece:
                count += 1
            else:
                break

        # West
        for col in reversed(range(self.move[1])):
            if self.board.board[(self.move[0], col)] == player.piece:
                count += 1
            else:
                break

        if count == chain:
            return True

        count = 0
        # North West
        for row, col in zip(reversed(range(self.move[0])),
                            reversed(range(self.move[1]))):
            if self.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        # South East
        for row, col in zip(range(self.move[0], self.board.dimension),
                            range(self.move[1], self.board.dimension)):
            if self.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        if count == chain:
            return True

        count = 0
        # North East
        for row, col in zip(reversed(range(self.move[0])),
                            range(self.move[1] + 1, self.board.dimension)):
            if self.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        # South West
        for row, col in zip(range(self.move[0], self.board.dimension),
                            reversed(range(self.move[1] + 1))):
            if self.board.board[(row, col)] == player.piece:
                count += 1
            else:
                break

        if count == chain:
            return True

        return False
