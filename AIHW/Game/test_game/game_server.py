from operator import itemgetter
import string
import os
import json
import time
from copy import deepcopy
import re
from myagent import run
from newgame import newgame
from calibrate import calibrate

class ReadInput(object):
    def __init__(self):
        self._matrix_size = None
        self._algo_type = None
        self._player_symbol = None
        self._total_time = None
        self._cell_values = list()
        self._board_state = list()

    @property
    def matrix_size(self):
        return self._matrix_size

    @property
    def algo_type(self):
        return self._algo_type

    @property
    def player_symbol(self):
        return self._player_symbol

    @property
    def total_time(self):
        return self._total_time

    @property
    def cell_values(self):
        return self._cell_values

    @property
    def board_state(self):
        return self._board_state

    def read(self):
        with open("input.txt", "r") as fp:
            lines = fp.readlines()
            self._matrix_size = int(lines[0].strip())
            self._algo_type = lines[1].strip()
            self._player_symbol = lines[2].strip()
            self._total_time = float(lines[3].strip())

            cell_start_line = 4
            for i in xrange(0, self.matrix_size):
                split_text = str(lines[cell_start_line+i]).split()
                row_val = list()
                for x in split_text:
                    row_val.append(int(x))
                self._cell_values.append(row_val)

            board_start_line = 4 + self.matrix_size
            for i in xrange(0, self.matrix_size):
                board_text = str(lines[board_start_line + i]).strip()
                row_val = list()
                for character in board_text:
                    row_val.append(character)
                self._board_state.append(row_val)

    def read_from_json(self, file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def write_json_to_text_file(self, file_path, json_data):
        if json_data:
            with open(file_path, 'w') as fp:
                json.dump(json_data, fp)
                fp.close()

class AlphaBetaAlgo(object):
    def __init__(self, player_symbol, depth, cell_values, board_state, board_size):
        self._player_symbol = player_symbol
        self._opponent_symbol = "X" if player_symbol == "O" else "O"
        self._depth = depth
        self._cell_values = cell_values
        self._board_state = board_state
        self._board_size = board_size
        self._best_row = -1
        self._best_col = -1
        self._best_move_type = ''
        self._alpha_num_mapping = self.get_alpha_num_dict()

    @property
    def player_symbol(self):
        return self._player_symbol

    @property
    def opponent_symbol(self):
        return self._opponent_symbol

    @property
    def depth(self):
        return self._depth

    @property
    def cell_values(self):
        return self._cell_values

    @property
    def board_state(self):
        return self._board_state

    @property
    def board_size(self):
        return self._board_size

    @property
    def alpha_num_mapping(self):
        return self._alpha_num_mapping

    @alpha_num_mapping.setter
    def alpha_num_mapping(self, value):
        self._alpha_num_mapping = value

    @property
    def best_row(self):
        return self._best_row
    
    @best_row.setter
    def best_row(self, value):
        self._best_row = value

    @property
    def best_col(self):
        return self._best_col
    
    @best_col.setter
    def best_col(self, value):
        self._best_col = value

    @property
    def best_move_type(self):
        return self._best_move_type
    
    @best_move_type.setter
    def best_move_type(self, value):
        self._best_move_type = value
    
    def print_board(self, board):
        for row in board:
            print ''.join(row)
            pass            

    def print_cell_values(self):
        for row in self.cell_values:
            #print ''.join(str(row))
            pass
            
    def get_alpha_num_dict(self):
        result = dict()
        for index,val in enumerate(string.ascii_uppercase):
            result[index+1]=val
        return result

    def write_to_output(self, move, board):
        with open("output.txt", "w") as fp:
            fp.write(move+'\n')
            for row in board:
                fp.write(''.join(row))
                fp.write('\n')

    def min_max_search(self):
        self.max_value(self.board_state, -10000, 10000, self.depth)        
        move = self.alpha_num_mapping[self.best_col+1]+str(self.best_row+1)+" "+self.best_move_type
        action = [self.best_row, self.best_col, self.best_move_type, self.player_symbol]
        return (action, move)

    def take_alphabeta_action(self, action, move):
        new_board = self.new_state_based_on_action(self.board_state, action, self.player_symbol)
        self.print_board(new_board)
        #print action
        self.write_to_output(move, new_board)

    def simple_matrix_copy(self, state):
        new_state = list()
        for i in xrange(0, self.board_size):
            new_state.append(['.']*self.board_size)
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                new_state[i][j] = state[i][j]
        return new_state
        
        
    def get_score(self, board):
        player_score = 0
        opponent_score = 0
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if board[i][j] == self.player_symbol:
                    player_score = player_score + self.cell_values[i][j]
                elif board[i][j] == self.opponent_symbol:
                    opponent_score = opponent_score + self.cell_values[i][j]
        return player_score - opponent_score

    def is_game_over(self, board):
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if board[i][j] == ".":
                    return False
        return True


    def terminal_test(self, state, depth):
        if depth == 0 or self.is_game_over(state):
            return True
        else:
            return False

    def new_state_based_on_action(self, board, action, symbol):
        i = action[0]
        j = action[1]
        move_type = action[2]
        board[i][j] = symbol
        if move_type == "Raid":
            if (j-1 > -1) and (board[i][j-1] == self.get_opposite_symbol(symbol)):
                board[i][j-1] = symbol
            if (j+1 < self.board_size) and (board[i][j+1] == self.get_opposite_symbol(symbol)):
                board[i][j+1] = symbol
            if (i-1 > -1) and (board[i-1][j] == self.get_opposite_symbol(symbol)):
                board[i-1][j] = symbol
            if (i+1 < self.board_size) and (board[i+1][j] == self.get_opposite_symbol(symbol)):
                board[i+1][j] = symbol
        return board


    def is_neighbour(self, i, j, board, symbol):
        if ((j-1 > -1) and (board[i][j-1] == symbol))\
            or ((j+1 < self.board_size) and (board[i][j+1] == symbol))\
            or ((i-1 > -1) and (board[i-1][j] == symbol))\
            or ((i+1 < self.board_size) and (board[i+1][j] == symbol)):
            return True

    def find_total_captured_val(self, i, j, board, symbol):
        total = self.cell_values[i][j]
        if (j-1 > -1) and (board[i][j-1] == self.get_opposite_symbol(symbol)):
            total = total + self.cell_values[i][j-1]
        if (j+1 < self.board_size) and (board[i][j+1] == self.get_opposite_symbol(symbol)):
            total = total + self.cell_values[i][j+1]
        if (i-1 > -1) and (board[i-1][j] == self.get_opposite_symbol(symbol)):
            total = total + self.cell_values[i-1][j]
        if (i+1 < self.board_size) and (board[i+1][j] == self.get_opposite_symbol(symbol)):
            total = total + self.cell_values[i+1][j]
        return total


    def get_opposite_symbol(self, symbol):
        if symbol == "X":
            return "O"
        elif symbol == "O":
            return "X"
        return "."


    def possible_actions(self, board, symbol, func_name):
        # Possible stake moves
        stakes = list()
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if board[i][j] == ".":
                    stakes.append([i,j, 'Stake', self.cell_values[i][j]])
        
        # Possible raid moves
        raids = list()
        for val in stakes:
            i = val[0]
            j = val[1]
            opposite_symbol = self.get_opposite_symbol(symbol)
            if self.is_neighbour(i, j, board, symbol) and self.is_neighbour(i, j, board, opposite_symbol):
                total_capture = self.find_total_captured_val(i, j, board, symbol)
                raids.append([i, j, 'Raid', total_capture])

        raids.extend(stakes)
        raids = sorted(raids, key=itemgetter(3), reverse=True)
        return raids
        
    def max_value(self, state, alpha, beta, depth):
        if self.terminal_test(state, (depth)):
            return self.get_score(state)

        v = -10000
        for action in self.possible_actions(state, self.player_symbol, "max_value"):
            copy_state = self.simple_matrix_copy(state)
            new_state = self.new_state_based_on_action(copy_state, action, self.player_symbol)
            new_v = self.min_value(new_state, alpha, beta, depth-1)
            v = max(v, new_v)
            if v >= beta:
                return v
            if alpha < v:
                alpha = v
                if self.depth == depth:
                    self.best_row = action[0]
                    self.best_col = action[1]
                    self.best_move_type = action[2]
        return v

    def min_value(self, state, alpha, beta, depth):
        if self.terminal_test(state, depth):
            return self.get_score(state)

        v = 10000
        for action in self.possible_actions(state, self.opponent_symbol, "min_value"):
            copy_state = self.simple_matrix_copy(state)
            new_state = self.new_state_based_on_action(copy_state, action, self.opponent_symbol)
            new_v = self.max_value(new_state, alpha, beta, depth-1)
            v = min(v, new_v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


class GameServer(object):
    def __init__(self):
        pass

    def is_game_over(self, board, matrix_size):
        for i in xrange(0, matrix_size):
            for j in xrange(0, matrix_size):
                if board[i][j] == ".":
                    return False
        return True

    def get_score(self, board, board_size, player_symbol, opponent_symbol, cell_values):
        player_score = 0
        opponent_score = 0
        for i in xrange(0, board_size):
            for j in xrange(0, board_size):
                if board[i][j] == player_symbol:
                    player_score = player_score + cell_values[i][j]
                elif board[i][j] == opponent_symbol:
                    opponent_score = opponent_score + cell_values[i][j]
        return player_score - opponent_score

    
    def read_output(self, matrix_size):
         with open("output.txt", "r") as fp:
            lines = fp.readlines()
            board_state = list()
            move = str(lines[0])
            for i in xrange(0, matrix_size):
                board_text = str(lines[i+1]).strip()
                row_val = list()
                for character in board_text:
                    row_val.append(character)
                board_state.append(row_val)
            return (move, board_state)

    def write_json_to_text_file(self, file_path, json_data):
        if json_data:
            with open(file_path, 'w') as fp:
                json.dump(json_data, fp)
                fp.close()

    def read_from_json(self, file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def write_to_input_file(self, matrix_size, move_type, symbol, total_time, cell_values, board):
        with open("input.txt", 'w') as fp:
            fp.write(str(matrix_size)+'\n')
            fp.write(str(move_type)+'\n')
            fp.write(symbol+'\n')
            fp.write(str(total_time)+'\n')
            for row in cell_values:
                txt = ''
                for col in row:
                    txt = txt + str(col)+" "
                fp.write(txt)
                fp.write('\n')
            for row in board:
                fp.write(''.join(row))
                fp.write('\n')


    def get_coordinates(self, alpha_num):
        result = dict()
        match_alpha = re.search("(^[A-Z]).*", alpha_num)
        match_num = re.search("([0-9].*$).*", alpha_num)
        if (not match_alpha) and (not match_num):
            raise Exception("Output Alpha num not matching.. Check output")

        alpha_num = dict()
        for index,val in enumerate(string.ascii_uppercase):
            alpha_num[val] = index+1
        
        i = int(match_num.group(0)) - 1
        j = int(alpha_num[match_alpha.group(1)]) - 1
        return (i, j)

    def is_neighbour(self, i, j, board, symbol, board_size):
        if ((j-1 > -1) and (board[i][j-1] == symbol))\
            or ((j+1 < board_size) and (board[i][j+1] == symbol))\
            or ((i-1 > -1) and (board[i-1][j] == symbol))\
            or ((i+1 < board_size) and (board[i+1][j] == symbol)):
            return True

    def validate_move(self, move, cur_board, prev_board, symbol, board_size):
        parse_move = move.split()
        (i, j) = self.get_coordinates(parse_move[0])
        move_type = parse_move[1]

        # Check if current position is empty
        if prev_board[i][j] != ".":
            raise Exception("Not empty")

        opp_symbol = "O" if symbol == "X" else "X"

        if move_type == "Raid":
            if not (self.is_neighbour(i, j, prev_board, symbol, board_size)\
                and self.is_neighbour(i, j, prev_board, opp_symbol, board_size)):
                raise Exception("Improper raise move")

        if move_type == "Stake":
            for x in xrange(0, board_size):
                for y in xrange(0, board_size):
                    if cur_board[x][y] != prev_board[x][y]:
                        if (x == i) and (y == j):
                            if cur_board[x][y] != symbol:
                                raise Exception("Stake move improper on board")
                        else:
                            raise Exception("Stake move not matching two boards")
                        

        if move_type == "Raid":
            prev_board[i][j] = symbol            
            if (j-1 > -1) and (prev_board[i][j-1] == opp_symbol):
                prev_board[i][j-1] = symbol
            if (j+1 < board_size) and (prev_board[i][j+1] == opp_symbol):
                prev_board[i][j+1] = symbol
            if (i-1 > -1) and (prev_board[i-1][j] == opp_symbol):
                prev_board[i-1][j] = symbol
            if (i+1 < board_size) and (prev_board[i+1][j] == opp_symbol):
                prev_board[i+1][j] = symbol

            for x in xrange(0, board_size):
                for y in xrange(0, board_size):
                    if cur_board[x][y] != prev_board[x][y]:
                        raise Exception("Raid move improper")

               
    def start(self):
        newgame()
        calibrate()
        
        read_input = ReadInput()
        read_input.read()
        
        board = read_input.board_state
        player_symbol = read_input.player_symbol
        matrix_size = read_input.matrix_size
        cell_values = read_input.cell_values
        total_time = read_input.total_time
        count = 0
        opponent_symbol = 'X' if read_input.player_symbol == "O" else "O"
        
        opponent_time = 0
        my_time = 0
        
        while not self.is_game_over(board, matrix_size):
            prev_board = deepcopy(board)
            start_time = time.time()
            print "Alpha Beta"
            minmax = AlphaBetaAlgo(opponent_symbol, 4,\
                                   cell_values, board, matrix_size)
            (action, move) = minmax.min_max_search()
            minmax.take_alphabeta_action(action, move)
            opponent_time = opponent_time + int((time.time() - start_time) * 1000)

            (move, board) = self.read_output(matrix_size)
            self.validate_move(move, board, prev_board, opponent_symbol, matrix_size)
            self.write_to_input_file(matrix_size, "COMPETITION", player_symbol, total_time, cell_values, board)
            
            if self.is_game_over(board, matrix_size):
                score = self.get_score(board, matrix_size, player_symbol, opponent_symbol, cell_values)
                print "Stopping the game.... FUll"
                print "Score :", score
                print "Opponents Time:", opponent_time
                print "My Time:", my_time
                return

            print "======================"
            prev_board = deepcopy(board)
            print "Clever Agent"
            start_time = time.time()
            run()
            #print "Actual Run time: ", int((time.time() - start_time) * 1000)
            my_time = my_time + int((time.time() - start_time) * 1000)
            #print "My total used time: ", my_time
            
            (move, board) = self.read_output(matrix_size)
            self.validate_move(move, board, prev_board, player_symbol, matrix_size)
            self.write_to_input_file(matrix_size, "COMPETITION", player_symbol, total_time, cell_values, board)
            
            score = self.get_score(board, matrix_size, player_symbol, opponent_symbol, cell_values)
            print "Score :", score
            print "===================================================================="
        print "Opponents Time:", opponent_time
        print "My Time:", my_time
        

def main():
    gs = GameServer()
    gs.start()

if __name__ == "__main__":
    main()