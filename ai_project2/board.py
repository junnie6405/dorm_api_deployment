from player import Player
from gamestate import GameState
import array
import copy

# Class to represent a Connect-4 game board (or Connect-2 or -3, or a different number).
# Because we are creating a lot of boards, using bytes instead of ints will save memory.
# NOTE: The board is stored so row 0 is the lowest level of the board, and row-1 is the
# top level.  So whenever we print the board, we print row-1 first, and end with row 0.
class Board:

    def __init__(self, r, c, inarow, prev_board=None, column_to_drop=None):
        """Create a new board."""
        self.num_rows = r
        self.num_cols = c
        self.consec_to_win = inarow

        # making a blank board?
        if prev_board is None:
            self.lowest_free_row = [0] * self.num_cols
            self.board = [array.array('b', [0] * self.num_cols) for _ in range(self.num_rows)]
            self.player_to_move = Player.MAX
            self.is_board_full = False
            self.moves_made_so_far = 0
            self.game_state = GameState.IN_PROGRESS

        # making move on existing board?
        else:
            if prev_board.is_column_full(column_to_drop):
                raise RuntimeError("Board is full in column " + column_to_drop)

            # copy the board
            self.board = copy.deepcopy(prev_board.board)

            # copy the free rows array
            self.lowest_free_row = copy.deepcopy(prev_board.lowest_free_row)

            self.player_to_move = prev_board.player_to_move.other_player()

            # make the move
            row_of_new_token = self.lowest_free_row[column_to_drop]
            if prev_board.get_player_to_move_next() == Player.MAX:
                self.board[row_of_new_token][column_to_drop] = 1
            else:
                self.board[row_of_new_token][column_to_drop] = -1

            self.lowest_free_row[column_to_drop] += 1
            self.moves_made_so_far = prev_board.moves_made_so_far + 1

            self.is_board_full = (self.moves_made_so_far == self.num_cols * self.num_rows)
            self.game_state = self.calc_state_of_game()

        # cache hash code
        self.hash_code = hash(self.__str__())

    def heuristic(self):
        max_count = 0
        min_count = 0
        for r in range(0, self.num_rows):
            for c in range(0, self.num_cols):
                if self.board[r][c] == 0:
                    continue
                total_sum = 0
                row_val = self.count_rows(r, c, self.board[r][c])
                col_val = self.count_cols(r, c, self.board[r][c])
                diag_up_val = self.count_diag_up(r, c, self.board[r][c])
                diag_down_val = self.count_diag_down(r, c, self.board[r][c])

                total_sum = row_val + col_val + diag_up_val + diag_down_val
                if self.board[r][c] == 1:
                    max_count += total_sum
                else:
                    min_count += total_sum

        if max_count > min_count:
            return max_count

        elif min_count > max_count:
            return -1 * min_count

        else:  # no optimal move.
            return 0

    def count_diag_down(self, row, col, cur_player):
        val = 0
        while row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1] == cur_player:
            if val == 0:  # two in a row
                val += 3
            elif val == 3:  # three in a row
                val += 7
            row -= 1
            col -= 1
        return val

    def count_diag_up(self, row, col, cur_player):
        val = 0
        while row + 1 < self.num_rows and col + 1 < self.num_cols and self.board[row + 1][col + 1] == cur_player:
            if val == 0:  # two in a row
                val += 3
            elif val == 3:  # three in a row
                val += 7
            row += 1
            col += 1
        return val

    def count_cols(self, row, col, cur_player):
        val = 0
        while col + 1 < self.num_cols and self.board[row][col + 1] == cur_player:
            if val == 0: # two in a row
                val += 3
            elif val == 3: # three in a row
                val += 7
            col += 1
        return val

    def count_rows(self, row, col, cur_player):
        val = 0
        while row + 1 < self.num_rows and self.board[row + 1][col] == cur_player:
            if val == 0: # two in a row
                val += 3
            elif val == 3: # three in a row
                val += 7
            row += 1
        return val

    def calc_state_of_game(self):
        """Only used by constructor to figure out win/loss/tie."""
        # check for wins
        for r in range(0, self.num_rows):
            for c in range(0, self.num_cols):
                if self.board[r][c] == 0:
                    continue

                if ((c <= self.num_cols - self.consec_to_win and self.all_match_in_a_row(r, c))
                    or (r <= self.num_rows - self.consec_to_win and self.all_match_in_a_col(r, c))
                    or (r <= self.num_rows - self.consec_to_win and c <= self.num_cols - self.consec_to_win and self.all_match_in_ne_diag(r, c))
                    or (r <= self.num_rows - self.consec_to_win and c - self.consec_to_win >= -1 and self.all_match_in_nw_diag(r, c))):

                    if self.board[r][c] == 1:
                        return GameState.MAX_WIN
                    elif self.board[r][c] == -1:
                        return GameState.MIN_WIN

        # if we get here, there was no win, so either it's a tie or in progress.
        if self.is_board_full:
            return GameState.TIE
        else:
            return GameState.IN_PROGRESS

    def make_move(self, col):
        """Make a move on this board and return a new board with the updated move (old board doesn't change)."""
        return Board(self.num_rows, self.num_cols, self.consec_to_win,
                     self, col)

    def is_column_full(self, col):
        """Determine if a column is full or not."""
        return self.lowest_free_row[col] == self.num_rows

    def get_player_to_move_next(self):
        return self.player_to_move

    def get_rows(self):
        return self.num_rows

    def get_cols(self):
        return self.num_cols

    def get_number_of_moves(self):
        return self.moves_made_so_far

    def get_game_state(self):
        return self.game_state

    def get_winner(self):
        """Return the winner if there is one."""
        if self.game_state == GameState.IN_PROGRESS:
            raise RuntimeError("Can't get winner for game in progress.")
        elif self.game_state == GameState.TIE:
            raise RuntimeError("Can't get winner for tie game.")
        elif self.game_state == GameState.MAX_WIN:
            return Player.MAX
        else:
            return Player.MIN

    def has_winner(self):
        return self.game_state == GameState.MAX_WIN or self.game_state == GameState.MIN_WIN

    def to_2d_string(self):
        sb = ""
        for r in range(self.num_rows - 1, -1, -1):
            for c in range(0, self.num_cols):
                if self.board[r][c] == 1:  # max is 1
                    sb += "X "
                elif self.board[r][c] == -1:  # min is -1
                    sb += "O "
                else:
                    sb += ". "
            sb += "\n"

        sb += "0 1 2 3 4 5 6 7 8 9"[0:self.num_cols * 2]
        return sb

    def __str__(self):
        sb = ""
        for r in range(self.num_rows - 1, -1, -1):
            for c in range(0, self.num_cols):
                if self.board[r][c] == 1:  # max is 1
                    sb += "X"
                elif self.board[r][c] == -1:  # min is -1
                    sb += "O"
                else:
                    sb += "."
            sb += "|"
        return sb

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return self.hash_code

    # internal functions below for detecting wins

    def all_match_in_a_row(self, row, startcol):
        for x in range(0, self.consec_to_win - 1):
            if self.board[row][startcol + x] != self.board[row][startcol + x + 1]:
                return False
        return True

    def all_match_in_a_col(self, startrow, col):
        for x in range(0, self.consec_to_win - 1):
            if self.board[startrow + x][col] != self.board[startrow + x + 1][col]:
                return False
        return True

    def all_match_in_ne_diag(self, startrow, startcol):
        for x in range(0, self.consec_to_win - 1):
            if self.board[startrow + x][startcol + x] != self.board[startrow + x + 1][startcol + x + 1]:
                return False
        return True

    def all_match_in_nw_diag(self, startrow, startcol):
        for x in range(0, self.consec_to_win - 1):
            if self.board[startrow + x][startcol - x] != self.board[startrow + x + 1][startcol - x - 1]:
                return False
        return True

