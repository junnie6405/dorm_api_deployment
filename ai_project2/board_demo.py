import player
from board import Board
from gamestate import GameState
from player import Player
def main():
	board = Board(4,4,3)

	board = board.make_move(0)
	board = board.make_move(1)
	board = board.make_move(0)
	board = board.make_move(1)
	board = board.make_move(0)
	board = board.make_move(1)

	print(board.to_2d_string())
	board.testing()

	"""
	
	
	first_turn = int(input("Who plays first?"))

	if first_turn == 2:
		board.player_to_move = Player.MIN
	else:
		board.player_to_move = Player.MAX

	while board.get_game_state() == GameState.IN_PROGRESS:
		print("The Current Board: ")
		print(board)
		if board.player_to_move == Player.MAX:
			current_player = "MAX"
		else:
			current_player = "MIN"

		print("It is {}'s turn".format(current_player))

		if current_player == "MAX":
			move = int(input("Computer chooses move: "))
		else:
			move = int(input("Enter Move: "))

		board = board.make_move(move)

	print("Final Board: ")
	print(board.to_2d_string())

	game_state = board.get_game_state()
	if game_state == GameState.MAX_WIN:
		print("MAX Wins")
	elif game_state == GameState.MIN_WIN:
		print("MIN Wins")
	else:
		print("Tie")
	"""
main()
