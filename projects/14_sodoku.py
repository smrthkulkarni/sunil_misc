"""
Backtracking
Solving sodoku
"""

class Sodoku(object):
    def __init__(self):
        self.board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                      [5, 2, 0, 0, 0, 0, 0, 0, 0],
                      [0, 8, 7, 0, 0, 0, 0, 3, 1],
                      [0, 0, 3, 0, 1, 0, 0, 8, 0],
                      [9, 0, 0, 8, 6, 3, 0, 0, 5],
                      [0, 5, 0, 0, 9, 0, 6, 0, 0],
                      [1, 3, 0, 0, 0, 0, 2, 5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 7, 4],
                      [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    def row_safe(self, x, y, val):
        for i in xrange(0,9):
            if self.board[x][i] == val:
                return False
        return True

    def col_safe(self, x, y, val):
        for i in xrange(0,9):
            if self.board[i][y] == val:
                return False
        return True

    def box_safe(self, x, y, val):
        for j in xrange(0, 3):
            for k in xrange(0,3):
                if(self.board[x + j][y + k] == val):
                    return False
        return True


    def is_safe(self, x, y, val):
        if self.row_safe(x, y, val) and\
            self.col_safe(x, y, val) and\
            self.box_safe(x-(x%3), y-(y%3), val):
            return True
        return False

    def find_next_empty_cell(self):
        for i in xrange(0, 9):
            for j in xrange(0, 9):
                if self.board[i][j] == 0:
                    return (i, j)

    def is_all_assigned(self):
        for i in xrange(0, 9):
            for j in xrange(0, 9):
                if self.board[i][j] == 0:
                    return False
        return True
        

    def sodoku_util(self):
        if self.is_all_assigned():
            return True
        x, y = self.find_next_empty_cell()
        for val in xrange(1,10):
            if self.is_safe(x, y, val):
                self.board[x][y] = val
                if self.sodoku_util():
                    return True
                self.board[x][y] = 0
        return False
                

    def print_sodoku(self):
        for i in xrange(0, 9):
            for j in xrange(0, 9):
                print self.board[i][j], 
            print ""

    def sodoku(self):
        if self.sodoku_util():
            self.print_sodoku()
        else:
            print "No solution"

def main():
    sudo = Sodoku()
    sudo.sodoku()

if __name__ == "__main__":
    main()

        


