from enum import Enum

class Player(Enum):
    MAX = 1
    MIN = -1

    def other_player(self):
        if self == Player.MIN:
            return Player.MAX
        else:
            return Player.MIN


        print("The transposition table has {} states".format(len(transposition_table)))
        if return_val[0] != 0:
            print("The first player has a guaranteed win with perfect play.")
        else:
            print("Neither player has a guaranteed win; game will end in tie with perfect play on both sides.")
        if debug:
            print("Transposition table: ")
            for key in transposition_table:
                print(key, "-> MinimaxInfo", transposition_table[key])
