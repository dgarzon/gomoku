import copy
from board import *


class State(object):
    def __init__(self):
        super(State, self).__init__()
        self.move = (0, 0)
        self.board = Board()
        self.parent = None

    def heuristic(self, game):
        flag = None

        if self.isWinner(game.current, game.chain):
            flag = True
        if self.isWinner(game.oponent, game.chain):
            flag = True

        current_chain_count = self.countChains(game.current)
        oponent_chain_count = self.countChains(game.oponent)

        if game.minimax_val == 2:  # MAX
            # self.board.printBoard()
            # print(current_chain_count, oponent_chain_count)
            # input("Enter..")
            if flag is True:
                return int(1000)
            if current_chain_count >= oponent_chain_count:
                return int(current_chain_count)
            elif current_chain_count == oponent_chain_count == game.chain - 1:
                return int(1000)
            else:
                return int(-oponent_chain_count)
        else:  # MIN
            if flag is True:
                return int(-1000)
            if current_chain_count > oponent_chain_count:
                return int(-current_chain_count)
            elif current_chain_count == oponent_chain_count == game.chain - 1:
                return int(-1000)
            else:
                return int(-oponent_chain_count)

    def counter(self, player, row, col, dir_x, dir_y):
        count = 0

        r = row + dir_x
        c = col + dir_y

        while r >= 0 and r < self.board.dimension and c >= 0 and\
                c < self.board.dimension:
            if self.board.board[(r, c)] == player.piece:
                count += 1
                r += dir_x
                c += dir_y
            else:
                break

        return count

    def countChains(self, player):
        max_chain = 0

        for row in range(self.board.dimension):
            for col in range(self.board.dimension):
                vertical_down = self.counter(player, row, col, 1, 0)
                vertical_up = self.counter(player, row, col, -1, 0)
                horizontal_right = self.counter(player, row, col, 0, 1)
                horizontal_left = self.counter(player, row, col, 0, 1)
                diagonal_1 = self.counter(player, row, col, 1, 1)
                diagonal_2 = self.counter(player, row, col, -1, 1)
                diagonal_3 = self.counter(player, row, col, 1, -1)
                diagonal_4 = self.counter(player, row, col, -1, -1)
                max_chain = max(max_chain, vertical_up, vertical_down,
                                horizontal_right, horizontal_left,
                                diagonal_1, diagonal_2,
                                diagonal_3, diagonal_4)

        return max_chain

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
