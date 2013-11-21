import random

class Board(object):
    def __init__(self):
        super(Board, self).__init__()
        self.board = {}
        self.dimension = None

    def initializeBoard(self, dimension):
        self.dimension = dimension

        for row in range(dimension):
            for col in range(dimension):
                self.board[(row, col)] = '.'

    def printBoard(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
                if (row, col) in self.board:
                    print(self.board[(row, col)], end=" ")
                else:
                    print(" ", end=" ")
            print("\n", end="")

    def makeMove(self, move, player):
        if self.isValidMove(move):
            self.board[(move[0], move[1])] = player.piece
            return move
        else:
            return (-1, -1)

    def isValidMove(self, move):
        if move[0] >= 0 and move[0] < self.dimension  and move[1] >= 0 and move[1] < self.dimension:
            if self.board[(move[0], move[1])] == '.':
                return True
            else:
                return False
        return False

    def randomMove(self):
        valid = self.getValidMoves()

        rand = random.randint(0, len(valid))

        return valid[rand]

    def getCloseMoves(self, row, col):
        moves = [(row - 1, col), (row + 1, col), (row, col + 1), (row, col - 1), (row + 1, col + 1), (row - 1, col - 1)]

        return moves


    def closeMove(self, move):
        close = self.getCloseMoves(move[0], move[1])

        rand = random.randint(0, len(close) - 1)

        move = close[rand]

        while self.isValidMove(move) is False:
            rand = random.randint(0, len(close) - 1)
            move = close[rand]

        return move


    def getValidMoves(self):
        valid = []
        for row in range(self.dimension):
            for col in range(self.dimension):
                move = (row, col)
                if self.isValidMove(move):
                    valid.append(move)

        # return reversed(valid)
        return valid
