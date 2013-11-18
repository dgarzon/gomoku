import sys
from gomoku import *


def main():
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <board dimension>\
                 <winning chain length> <time limit>' % sys.argv[0])

    game = Gomoku(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    game.displayMenu()
    game.mode = int(input("Choose Mode: "))
    game.start()

if __name__ == "__main__":
    main()
