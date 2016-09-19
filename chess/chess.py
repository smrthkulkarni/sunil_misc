"""
Design chess
"""

TOP = 'top_player'
BUTTOM = 'buttom_player'
WHITE = "white"

class ChessBoard(object):
	def __init__(self, white_pos=BOTTOM):
		self.board = self.assign_board()
		self.white_pos = white_pos
		self.white_pieces_list = get_white_pieces_list()
		self.black_pieces_list = get_black_pieces_list()

	def assign_board(self):
		board = dict()
		for i in xrange(8, 0, -1):
			for j in xrange(97, 105):
				board[chr(j)+str(i)] = chr(j)+str(i)
		return board

	def print_board(self):
		for i in xrange(8, 0, -1):
			for j in xrange(97, 105):
				print self.board[chr(j)+str(i)],
			print

	def get_white_pieces_list(self):
		white_pieces_list = []
		for j in xrange(97, 105):
			pos = j+str(1)
			self.board[pos] = Pieces(WHITE, pos, BOTTOM)
			white_pieces_list.append(self.board[pos])
		return white_pieces_list

	def get_black_pieces_list(self):
		black_pieces_list = []
		for j in xrange(97, 105):
			pos = j+str(6)
			self.board[pos] = Pieces(BLACK, pos, TOP)
			white_pieces_list.append(self.board[pos])
		return black_pieces_list

chess_board = ChessBoard()
chess_board.print_board()






class Pieces(object):
	def __init__(self, color, pos, player_seating):
		self._color = color
		self._pos = pos
		self.player_seating = player_seating

	def move(self):
		raise "Please implement the move function"

	def kill(self):
		raise "Please implement the kill function"

	def is_valid_move(self):
		raise "Please implement the is_valid_move function"

	def get_alpha_num(self):
		return self._pos[0], int(self._pos[1])

	def increment_alpha(self, alpha, num):
		return chr(ord(alpha) + num)

	def is_coordinates_inside_board(self, board, pos):
		if pos in board:
			return True
		return False

	def is_piece_present(self, board, pos):
		if board[pos]:
			return True
		return False

	def print_piece(self):
		raise "Please implement the print_piece function"

	def get_piece_name(self):
		raise "Please implement the get_piece_name function"		
		


class Pawn(Pieces):
	def __init__(self, color, pos, player_seating, short_name="P", description="Pawn"):
		super(Pawn, self).__init__(color, pos, player_seating)
		self.name = short_name
		self.description = description
		self.possible_moves = possible_kill_moves()
		self.possible_kill_moves = possible_valid_moves()

	def get_piece_name(self):
		return self.name


	def move(self, board, new_pos):
		if pos in self.possible_moves:
			board[self.pos] = None
			board[new_pos] = self
			self.pos = new_pos
			
		elif new_pos in self.possible_kill_moves:
			board[self.pos] = None
			board[new_pos] = self
			self.pos = new_pos
		else:
			return "Not a valid move"

		self.possible_moves = self.possible_valid_moves(board)
		self.possible_kill_moves = self.possible_kill_moves(board)


	def possible_kill_moves(self, board):
		# If the player is at buttom
		a = [1, -1]
		n = [1, 1]
		if self.player_seating == TOP:
			a = [1, -1]
			n = [-1, -1]
		possible_kill_moves = []
		for i in xrange(0, len(a)):
			possible_num = n[i] + num
			possible_alpha = self.increment_alpha(alpha, a[i])
			possible_move = possible_alpha + str(possible_num)
			if not is_coordinates_inside_board(board, possible_move):
				continue
			if self.is_piece_present(board, possible_move):
				possible_kill_moves.append(possible_move)
		return possible_kill_moves
		
	
	def possible_valid_moves(self, board):
		# If the player is at buttom
		a = [0, 0]
		n = [1, 2]
		if self.player_seating == TOP:
			a = [0, 0]
			n = [-1, -2]

		(alpha, num) = self.get_alpha_num()
		possible_moves = list()

		# Empty location moves
		for i in xrange(0, len(a)):
			possible_num = n[i] + num
			possible_alpha = self.increment_alpha(alpha, a[i])
			possible_move = possible_alpha + str(possible_num)
			if not is_coordinates_inside_board(board, possible_move):
				continue
			if self.is_piece_present(board, possible_move):
				break
			possible_moves.append(possible_move)
		return possible_moves

pwn = Pawn("White", "b2", BUTTOM)
pwn = pwn.possible_valid_moves()
 



