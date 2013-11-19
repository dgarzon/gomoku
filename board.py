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
        if self.board[(move[0], move[1])] == '.':
            return True
        return False

    def getValidMoves(self):
        valid = []
        for row in range(self.dimension):
            for col in range(self.dimension):
                move = (row, col)
                if self.isValidMove(move):
                    valid.append(move)

        # return reversed(valid)
        return valid
