from board import *


class State(object):
    def __init__(self):
        super(State, self).__init__()
        self.board = Board()
        self.parent = None
        self.children = []

    def heuristic(self):
        None

    def generateChildren(self, player):
        valid = self.board.getValidMoves()
        for move in valid:
            new_state = player.makeMove(self, move)
            self.children.append(new_state)
