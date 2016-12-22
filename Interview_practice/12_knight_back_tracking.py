"""
Backtracking using knights problem
The knight is placed on the first block of an empty board and, moving according to the rules of chess, must visit each square exactly once.
"""

class KnightMove(object):
	

	def is_valid(self,x, y, board):
		if (x<8 and y<8) and (x>-1 and y>-1) and not (board[x][y]):
			return True
		else:
			return False

	def next_move(self):
		return {'x' : [ 2, 1, -1, -2, -2, -1,  1,  2],
				'y' : [ 1, 2,  2,  1, -1, -2, -2, -1]
			}

	def assign_board(self):
		board_list = []
		for x in xrange(0,8):
			row = []
			for y in xrange(0,8):
				row.append(None)
			board_list.append(row)
		return board_list
	

	def knight_util(self, x, y, count, board):
		if count == 63:
			return True
		
		if (x ==0 and y==0):
			print (x, y, count)
		for k in xrange(0,8):
			next_x = x + self.next_move().get('x')[k]
			next_y = y + self.next_move().get('y')[k]
				
			if self.is_valid(next_x, next_y, board):
				board[next_x][next_y] = count
				count = count + 1
				if(self.knight_util(next_x, next_y, count, board)):
					return True					
				else:
					board[next_x][next_y] = None
		return False

	def knight(self):
		board = self.assign_board()
		self.print_board(board)
		board[0][0] = 0
		if self.knight_util(0,0,1, board):
			print "Successful"
			self.print_board(board)
		else:
			print "Not Successful"

	def print_board(self, board):
		for x in xrange(0,8):
			for y in xrange(0,8):
				print str(board[x][y]) + " ", 
			print

def main():
	km = KnightMove()
	km.knight()	

if __name__ == "__main__":
	main()