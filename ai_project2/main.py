#“I have neither given nor received unauthorized aid on this program.”

#I implemented my heuristic in board.py so please use my board.py file.

from board import Board
from collections import defaultdict
from gamestate import GameState
from player import Player

class pruning:
    vals = 0

def utility(board, game_state):
    if game_state == GameState.TIE:
        return 0

    util_val = board.num_rows * board.num_cols * 10000 / board.moves_made_so_far

    if game_state == GameState.MAX_WIN:
        return util_val
    else:
        return -1 * util_val

def mini_max(board, transposition_table):
    if board in transposition_table:
        return transposition_table[board]

    if board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(board, board.get_game_state())
        info = (util, None)
        transposition_table[board] = info
        return info

    turn = board.get_player_to_move_next()

    if turn == Player.MAX:
        v = float('-inf') #local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            # get a new board after making this move.
            new_board = board.make_move(move)
            child_info = mini_max(new_board, transposition_table)
            v2, action = child_info[0], child_info[1]
            if v2 > v:
                v = v2
                best_move = move

        info = (v, best_move)
        transposition_table[board] = info
        return info

    else:
        v = float('inf')  # local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            new_board = board.make_move(move)
            child_info = mini_max(new_board, transposition_table)
            v2, action = child_info[0], child_info[1]
            if v2 < v:
                v = v2
                best_move = move

        info = (v, best_move)
        transposition_table[board] = info
        return info


def alpha_beta(board, alpha, beta, transposition_table):

    if board in transposition_table:
        return transposition_table[board]

    if board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(board, board.get_game_state())
        info = (util, None)
        transposition_table[board] = info
        return info

    turn = board.get_player_to_move_next()

    if turn == Player.MAX:
        v = float('-inf') #local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            # get a new board after making this move.
            new_board = board.make_move(move)
            child_info = alpha_beta(new_board, alpha, beta, transposition_table)
            v2, action = child_info[0], child_info[1]

            if v2 > v:
                v = v2
                best_move = move
                alpha = max(alpha, v)

            if v >= beta:
                pruning.vals += 1
                return (v, best_move)

        info = (v, best_move)
        transposition_table[board] = info
        return info

    else:
        v = float('inf')  # local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            new_board = board.make_move(move)
            child_info = alpha_beta(new_board, alpha, beta, transposition_table)
            v2, action = child_info[0], child_info[1]
            if v2 < v:
                v = v2
                best_move = move
                beta = min(beta, v)

            if v <= alpha: # increment the # prune here too.
                pruning.vals += 1
                return (v, best_move)

        info = (v, best_move)
        transposition_table[board] = info
        return info

def alpha_beta_heuristics(board, alpha, beta, depth, transposition_table):

    if board in transposition_table:
        return transposition_table[board]

    if board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(board, board.get_game_state())
        info = (util, None)
        transposition_table[board] = info
        return info

    if depth == 0: #cutoff player looked ahead given amount of moves
        heuristic = board.heuristic()
        info = (heuristic, None)
        transposition_table[board] = info
        return info

    turn = board.get_player_to_move_next()

    if turn == Player.MAX:
        v = float('-inf') #local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            # get a new board after making this move.
            new_board = board.make_move(move)
            child_info = alpha_beta_heuristics(new_board, alpha, beta, depth - 1, transposition_table)
            v2, action = child_info[0], child_info[1]

            if v2 > v:
                v = v2
                best_move = move
                alpha = max(alpha, v)

            if v >= beta:
                pruning.vals += 1
                return (v, best_move)

        info = (v, best_move)
        transposition_table[board] = info
        return info

    else:
        v = float('inf')  # local max at the current depth
        best_move = None
        available_moves = []
        for i in range(board.num_cols):
            if not board.is_column_full(i):
                available_moves.append(i)

        for move in available_moves:
            new_board = board.make_move(move)
            child_info = alpha_beta_heuristics(new_board, alpha, beta, depth - 1, transposition_table)
            v2, action = child_info[0], child_info[1]
            if v2 < v:
                v = v2
                best_move = move
                beta = min(beta, v)

            if v <= alpha: # increment the # prune here too.
                return (v, best_move)

        info = (v, best_move)
        transposition_table[board] = info
        return info

def game_playing(board, transposition_table):

    first_turn = int(input("Who plays first? 1 = human 2 = computer"))
    game_board = board
    if first_turn == 1:
        max_player = 'human'
        min_player = 'computer'
    else:
        max_player = 'computer'
        min_player = 'human'

    cur_player_map = {'max': max_player, 'min': min_player}

    while game_board.get_game_state() == GameState.IN_PROGRESS:
        print("The Current Board: ")
        print(game_board.to_2d_string())
        if game_board.player_to_move == Player.MAX:
            current_player = cur_player_map['max']
        else:
            current_player = cur_player_map['min']

        if game_board not in transposition_table: # pruning happened here
            print("This state was previously pruned. Re-run alpha beta from here.")
            transposition_table = defaultdict(tuple)
            child_info = alpha_beta(game_board, float('-inf'), float('inf'), transposition_table)

        info = transposition_table[game_board]
        mini_max_val, action = info[0], info[1]

        print("Minimax value for this state: {}, optimal move: {}".format(mini_max_val, action))
        if game_board.player_to_move == Player.MAX:
            print("It is MAX's turn.")
        else:
            print("It is MIN's turn.")

        if current_player == "computer":
            print("computer chooses move {}".format(action))
            move = action
        else:
            move = int(input("Enter Move: "))
            print("user chooses move {}".format(move))

        game_board = game_board.make_move(move)

    print("Game Over!")
    print(game_board.to_2d_string())

    game_state = game_board.get_game_state()
    if game_state == GameState.MAX_WIN:
        print("The winner is MAX ({})".format(cur_player_map['max']))
    elif game_state == GameState.MIN_WIN:
        print("The winner is MIN ({})".format(cur_player_map['min']))
    else:
        print("Tie")

    replay = input("play again? (y/n): ")
    if replay == 'y':
        game_playing(board, transposition_table)

def game_playing_part_c(board, transposition_table, depth):

    first_turn = int(input("Who plays first? 1 = human 2 = computer"))
    game_board = board
    if first_turn == 1:
        max_player = 'human'
        min_player = 'computer'
    else:
        max_player = 'computer'
        min_player = 'human'

    cur_player_map = {'max': max_player, 'min': min_player}

    while game_board.get_game_state() == GameState.IN_PROGRESS:
        print("The Current Board: ")
        print(game_board.to_2d_string())
        if game_board.player_to_move == Player.MAX:
            current_player = cur_player_map['max']
            info = alpha_beta_heuristics(game_board, float('-inf'), float('inf'), depth, transposition_table)
        else:
            current_player = cur_player_map['min']
            info = transposition_table[game_board]

        mini_max_val, move = info[0], info[1]

        print("Minimax value for this state: {}, optimal move: {}".format(mini_max_val, move))
        if game_board.player_to_move == Player.MAX:
            print("It is MAX's turn.")
        else:
            print("It is MIN's turn.")

        if current_player == "computer":
            print("computer chooses move {}".format(move))
        else:
            move = int(input("Enter Move: "))
            print("user chooses move {}".format(move))

        game_board = game_board.make_move(move)

    print("Game Over!")
    print(game_board.to_2d_string())

    game_state = game_board.get_game_state()
    if game_state == GameState.MAX_WIN:
        print("The winner is MAX ({})".format(cur_player_map['max']))
    elif game_state == GameState.MIN_WIN:
        print("The winner is MIN ({})".format(cur_player_map['min']))
    else:
        print("Tie")

    replay = input("play again? (y/n): ")
    if replay == 'y':
        game_playing_part_c(board, transposition_table)

def main():
    print("Welcome to Connect 4 Game.")
    game_type = input("Would you like to run part A/B?C? (Type in Capital Letter) ")
    rows = int(input("Enter rows: "))
    cols = int(input("Enter cols: "))
    inarow = int(input("Enter number in a row to win: "))

    game_board = Board(rows, cols, inarow) # initialize our board
    debug = input("Do you want debugging info? Type y or n: ")
    transposition_table = defaultdict(tuple)

    if game_type == "A" or game_type == "B":
        if game_type == "A":
            return_val = mini_max(game_board, transposition_table)
        else:
            return_val = alpha_beta(game_board, float('-inf'), float('inf'), transposition_table)

        print("The transposition table has {} states".format(len(transposition_table)))

        if game_type == "B":
            print("The tree was pruned {} times".format(pruning.vals))

        if return_val[0] != 0:
            print("The first player has a guaranteed win with perfect play.")
        else:
            print("Neither player has a guaranteed win; game will end in tie with perfect play on both sides.")

        if debug == 'y':
            print("Transposition table: ")
            for key in transposition_table:
                print(key, "-> MinimaxInfo", transposition_table[key])

        game_playing(game_board, transposition_table) # let user and computer play game.

    else:
        depth = int(input("Number of moves to look ahead (depth): "))
        game_playing_part_c(game_board, transposition_table, depth)

if __name__ == "__main__":
    main()