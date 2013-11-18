class Board(object):
    """docstring for Board"""
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
        self.board[(move[0], move[1])] = player.piece

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

        return valid
