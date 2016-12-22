"""
Backtracking - Rat maze
Can only move forward & down
"""


class RatMaze(object):
	def __init__(self):
		self.maze = [[1, 0, 0, 0],
            [1, 1, 0, 1],
            [0, 1, 0, 0],
            [1, 1, 1, 1]
		]
		self.path_followed = [[None, None, None, None],
					 [None, None, None, None],
					 [None, None, None, None],
					 [None, None, None, None]]

	def is_valid(self, x, y):
		if x<4 and y<4 and self.maze[x][y] == 1:
			return True
		else:
			return False

	def rat_move_util(self, x, y):
		print x, y
		if x==3 and y==3:
			print ""
			return True
		if self.is_valid(x, y):
			self.path_followed[x][y] = 1
			if self.rat_move_util(x+1, y):
				return True
			if self.rat_move_util(x, y+1):
				return True
			self.path_followed[x][y] = None
			return False

	def print_path(self):
		for x in xrange(0,4):
			for y in xrange(0,4):
				print self.path_followed[x][y], 
			print ""

	def rat_move(self):
		if self.rat_move_util(0, 0):
			self.print_path()
		else:
			print "No path available"

def main():
	rat = RatMaze()
	rat.rat_move()	

if __name__ == "__main__":
	main()
