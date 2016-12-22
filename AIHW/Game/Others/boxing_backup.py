from operator import itemgetter
import string
import os
import json
import time

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
            

    def print_cell_values(self):
        for row in self.cell_values:
            print ''.join(str(row))
            

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
        print action
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

class ReadInput(object):
    def __init__(self):
        self._matrix_size = None
        self._algo_type = None
        self._player_symbol = None
        self._depth = None
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
    def depth(self):
        return self._depth

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
            self._depth = int(lines[3].strip())

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


class AlternateBoxStrategy(object):
    def __init__(self, board_size, board, cell_values, symbol, box_area=None):
        self.board_size = board_size
        self.board = board 
        self.cell_values = cell_values
        self.symbol = symbol
        self.opponent_symbol = "X" if symbol == "O" else "O"
        self.box_area = box_area
        self._alpha_num_mapping = self.get_alpha_num_dict()
        self.heuristic_table = cell_values

    @property
    def alpha_num_mapping(self):
        return self._alpha_num_mapping

    @alpha_num_mapping.setter
    def alpha_num_mapping(self, value):
        self._alpha_num_mapping = value

    def print_board(self, board):
        for row in board:
            print ''.join(row)
            
    def print_cell_values(self):
        for row in self.cell_values:
            print ''.join(str(row))



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

    def write_prev_state_output(self, board):
        with open("previous_state.txt", "w") as fp:
            for row in board:
                fp.write(''.join(row))
                fp.write('\n')

    def read_prev_state_output(self, matrix_size):
         with open("previous_state.txt", "r") as fp:
            lines = fp.readlines()
            board_state = list()
            for i in xrange(0, matrix_size):
                board_text = str(lines[i]).strip()
                row_val = list()
                for character in board_text:
                    row_val.append(character)
                board_state.append(row_val)
            return board_state

    def get_opposite_symbol(self, symbol):
        if symbol == "X":
            return "O"
        elif symbol == "O":
            return "X"
        return "."

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

    def box_strategy_output(self, i, j, move_type, player_symbol):
        move = self.alpha_num_mapping[j+1]+str(i+1)+ " "+ move_type
        action = [i, j, move_type, player_symbol]
        new_board = self.new_state_based_on_action(self.board, action, player_symbol)
        self.print_board(new_board)
        self.write_to_output(move, new_board)            

    def is_neighbours_unoccupied(self, i, j, board, symbol):
        if ((j-1 > -1) and (board[i][j-1] == symbol))\
            or ((j+1 < self.board_size) and (board[i][j+1] == symbol))\
            or ((i-1 > -1) and (board[i-1][j] == symbol))\
            or ((i+1 < self.board_size) and (board[i+1][j] == symbol)):
            return True

    def read_from_json(self, file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def write_json_to_text_file(self, file_path, json_data):
        if json_data:
            with open(file_path, 'w') as fp:
                json.dump(json_data, fp)
                fp.close()
        

    def find_max_square(self):
        if os.path.isfile('./top_boxing_coordinates.txt'):
            return self.read_from_json('./top_boxing_coordinates.txt')

        if self.board_size < 3:
            return None

        max_sq_matrix = self.simple_matrix_copy(self.cell_values)
        
        for i in xrange(0, self.board_size):
            col_sum = 0
            for j in xrange(0, self.board_size):
                if self.board[i][j] == self.opponent_symbol:
                    col_sum = col_sum - self.cell_values[i][j]
                    max_sq_matrix[i][j] = col_sum
                    continue
                col_sum = col_sum + self.cell_values[i][j]
                max_sq_matrix[i][j] = col_sum
        
        #print max_sq_matrix

        val_matrix_list = list()
        for i in xrange(2, self.board_size):
            for j in xrange(2, self.board_size):
                if (j-3 < 0):
                    val = max_sq_matrix[i][j] + max_sq_matrix[i-1][j] + max_sq_matrix[i-2][j]
                    val_matrix_list.append([i,j, val])
                else:
                    val = max_sq_matrix[i][j] + max_sq_matrix[i-1][j] + max_sq_matrix[i-2][j]\
                          - (max_sq_matrix[i][j-3] + max_sq_matrix[i-1][j-3] + max_sq_matrix[i-2][j-3])
                    val_matrix_list.append([i,j, val])
        
        num_boxing = 0    
        if self.board_size <= 5:
            num_boxing = 2
        if self.board_size <= 10:
            num_boxing = 4
        if self.board_size <= 15:
            num_boxing = 6
        if self.board_size <= 20:
            num_boxing = 8
        if self.board_size > 20:
            num_boxing = 10
        val_matrix_list = sorted(val_matrix_list, key=itemgetter(2), reverse=True)[:num_boxing]
        
        val_matrix_list = sorted(val_matrix_list, key=itemgetter(2), reverse=True)
        self.write_json_to_text_file('./top_boxing_coordinates.txt', val_matrix_list)
        return val_matrix_list
    
    def best_boxing_moves(self, box_i, box_j):
        co_ordinates = dict()
        co_ordinates["tl"] = (box_i - 2, box_j-2)
        co_ordinates["tm"] = (box_i - 2, box_j-1)
        co_ordinates["tr"] = (box_i - 2, box_j)
        co_ordinates["ml"] = (box_i - 1, box_j-2)
        co_ordinates["mm"] = (box_i - 1, box_j-1)
        co_ordinates["mr"] = (box_i - 1, box_j)
        co_ordinates["bl"] = (box_i, box_j-2)
        co_ordinates["bm"] = (box_i, box_j-1)
        co_ordinates["br"] = (box_i, box_j)

        pawn = dict()
        cell_val = dict()
        total_pawn = 0
        my_pawn_count = 0
        opponent_pawn_count = 0
        for key, val in co_ordinates.iteritems():
            cell_val[key] = self.cell_values[val[0]][val[1]]
            if self.board[val[0]][val[1]] == ".":
                pawn[key+"_pawn"] = 1
                total_pawn = total_pawn + 1
            elif self.board[val[0]][val[1]] == self.symbol:
                pawn[key+"_pawn"] = 2
                total_pawn = total_pawn + 2
                my_pawn_count = my_pawn_count + 1
            else:
                pawn[key+"_pawn"] = 0
                opponent_pawn_count = opponent_pawn_count + 1

        if my_pawn_count == 5 or (opponent_pawn_count + my_pawn_count > 4):
            return None

        possible_box = dict()
        possible_box["top_box"] = ["bl", "ml", "tm", "mr", "br"]
        possible_box["right_box"] = ["tl", "tm", "mr", "bm", "bl"]
        possible_box["left_box"] = ["tr", "tm", "ml", "bm", "br"]
        possible_box["bottom_box"] = ["tl", "ml", "bm", "mr", "tr"]

        priority_move_list = list()
        for boxes, box_list in possible_box.iteritems():
            total_val = 0
            total_pawn = 0
            max_val = 0
            max_co_ordinates = None
            for val in box_list:
                if not pawn[val+"_pawn"]:
                    total_pawn = 0
                    break
                if max_val < cell_val[val] \
                    and self.board[co_ordinates[val][0]][co_ordinates[val][1]] == '.':
                    max_val = cell_val[val]
                    max_co_ordinates = co_ordinates[val]
                total_val = total_val + cell_val[val]
                total_pawn = total_pawn + pawn[val+"_pawn"]
            if total_pawn:
                priority_move_list.append([boxes, total_val * total_pawn, max_co_ordinates])

        sorted_priority_move_list = sorted(priority_move_list,  key=itemgetter(1), reverse=True)

        return sorted_priority_move_list

    def is_safe_against_next_raids(self, i, j):
        if (i-1 > -1) and (j-1 > -1) and self.board[i-1][j-1] == self.opponent_symbol\
            and (self.board[i-1][j] == "." or self.board[i][j-1] == "."):
            return False

        if (i+1 < self.board_size) and (j-1 > -1) and self.board[i+1][j-1] == self.opponent_symbol\
            and (self.board[i][j-1] == "." or self.board[i+1][j] == "."):
            return False

        if (i-1 > -1) and (j+1 < self.board_size) and self.board[i-1][j+1] == self.opponent_symbol\
            and (self.board[i-1][j] == "." or self.board[i][j+1] == "."):
            return False

        if (i+1 < self.board_size) and (j+1 < self.board_size) and self.board[i+1][j+1] == self.opponent_symbol\
            and (self.board[i][j+1] == "." or self.board[i+1][j] == "."):
            return False

        if (j-2 > -1) and (self.board[i][j-2] == self.opponent_symbol and self.board[i][j-1] == "."):
            return False

        if (j+2 < self.board_size) and (self.board[i][j+2] == self.opponent_symbol and self.board[i][j+1] == "."):
            return False

        if (i-2 > -1) and (self.board[i-2][j] == self.opponent_symbol and self.board[i-1][j] == "."):
            return False

        if (i+2 < self.board_size) and (self.board[i+2][j] == self.opponent_symbol and self.board[i+1][j] == "."):
            return False
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


    def possible_raids(self, i, j):
        optimal_rides = list()
        if (i-1 > -1) and (j-1 > -1) and self.board[i-1][j-1] == self.symbol:
            if self.board[i-1][j] == ".":
                optimal_rides.append([i-1, j, self.find_total_captured_val(i-1, j, self.board, self.symbol)])
            elif self.board[i][j-1] == ".":
                optimal_rides.append([i, j-1, self.find_total_captured_val(i, j-1, self.board, self.symbol)])

        if (i+1 < self.board_size) and (j-1 > -1) and self.board[i+1][j-1] == self.symbol:
            if self.board[i][j-1] == ".":
                optimal_rides.append([i, j-1, self.find_total_captured_val(i, j-1, self.board, self.symbol)])
            elif self.board[i+1][j] == ".":
                optimal_rides.append([i+1, j, self.find_total_captured_val(i+1, j, self.board, self.symbol)])

        if (i-1 > -1) and (j+1 < self.board_size) and self.board[i-1][j+1] == self.symbol:
            if self.board[i-1][j] == ".":
                optimal_rides.append([i-1, j, self.find_total_captured_val(i-1, j, self.board, self.symbol)])
            elif self.board[i][j+1] == ".":
                optimal_rides.append([i, j+1, self.find_total_captured_val(i, j+1, self.board, self.symbol)])

        if (i+1 < self.board_size) and (j+1 < self.board_size) and self.board[i+1][j+1] == self.symbol:
            if self.board[i][j+1] == ".":
                optimal_rides.append([i, j+1, self.find_total_captured_val(i, j+1, self.board, self.symbol)])
            elif self.board[i+1][j] == ".":
                optimal_rides.append([i+1, j, self.find_total_captured_val(i+1, j, self.board, self.symbol)])

        if (j-2 > -1) and (self.board[i][j-2] == self.symbol and self.board[i][j-1] == "."):
            optimal_rides.append([i, j-1, self.find_total_captured_val(i, j-1, self.board, self.symbol)])
            
        if (j+2 < self.board_size) and (self.board[i][j+2] == self.symbol and self.board[i][j+1] == "."):
            optimal_rides.append([i, j+1, self.find_total_captured_val(i, j+1, self.board, self.symbol)])

        if (i-2 > -1) and (self.board[i-2][j] == self.symbol and self.board[i-1][j] == "."):
            optimal_rides.append([i-1, j, self.find_total_captured_val(i-1, j, self.board, self.symbol)])

        if (i+2 < self.board_size) and (self.board[i+2][j] == self.symbol and self.board[i+1][j] == "."):
            optimal_rides.append([i+1, j, self.find_total_captured_val(i+1, j, self.board, self.symbol)])

        return optimal_rides

    def simple_matrix_copy(self, state):
        new_state = list()
        for i in xrange(0, self.board_size):
            new_state.append(['.']*self.board_size)
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                new_state[i][j] = state[i][j]
        return new_state
        


    def is_neighbour(self, i, j, board, symbol):
        if ((j-1 > -1) and (board[i][j-1] == symbol))\
            or ((j+1 < self.board_size) and (board[i][j+1] == symbol))\
            or ((i-1 > -1) and (board[i-1][j] == symbol))\
            or ((i+1 < self.board_size) and (board[i+1][j] == symbol)):
            return True


    def take_move(self, i, j):
        if not self.board[i][j] == ".":
            print i, j
            raise Exception("Not a valid move check")

        if self.is_neighbour(i, j, self.board, self.symbol) and\
           self.is_neighbour(i, j, self.board, self.opponent_symbol):
           self.box_strategy_output(i, j, "Raid", self.symbol)
           print i, j, "Raid"
        else:
            self.box_strategy_output(i, j, "Stake", self.symbol)
            print i, j, "Stake"

    def get_possible_best_move_in_boxing(self):
        max_squares_list = self.find_max_square()
        for sq in max_squares_list:
            results = self.best_boxing_moves(sq[0], sq[1])
            if not results:
                continue
            for box_move in results:
                co_ordinates = box_move[2]
                i = co_ordinates[0]
                j = co_ordinates[1]
                if self.board[i][j] == "." and self.is_safe_against_next_raids(i, j):
                    self.take_move(i, j)
                    return True
        os.system("touch stop_boxing.txt")
        return False

    def find_prev_and_current_state_pos(self, prev_board, cur_board):
        changed_cordinates = list()
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if prev_board[i][j] != cur_board[i][j]:
                    changed_cordinates.append((i,j))
        return changed_cordinates

    def get_prev_current_changed_coordinates(self):
        if os.path.isfile('./previous_state.txt'):
            prev_board = self.read_prev_state_output(self.board_size)
            changed_cordinates = self.find_prev_and_current_state_pos(prev_board, self.board)
            return changed_cordinates
        return

    def raid_kill(self):
        raid_list = list()
        changed_cordinates = self.get_prev_current_changed_coordinates()
        if changed_cordinates:
            for co_ordinates in changed_cordinates:
                raids = self.possible_raids(co_ordinates[0], co_ordinates[1])
                if raids:
                    raid_list.extend(raids)
        if raid_list:
            raid_list = sorted(raid_list, key=itemgetter(2), reverse=True)
            for raid in raid_list:
                self.take_move(raid[0], raid[1])
                self.write_prev_state_output(self.board)
                return True
        return False

    def filled_unfilled_board_count(self):
        num_filled = 0
        num_unfilled = 0
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if self.board[i][j] == self.symbol:
                    num_filled = num_filled + 1
                elif self.board[i][j] == ".":
                    num_unfilled = num_unfilled + 1
        return (num_filled, num_unfilled)

    def write_diagonal_position_kill_txt(self, value_co_ordinates_list, monitor_kill_heuristic_table, heuristic_table):
        result = dict()
        result["value_co_ordinates_list"] = value_co_ordinates_list
        result["monitor_kill_heuristic_table"] = monitor_kill_heuristic_table
        result["heuristic_table"] = heuristic_table
        self.write_json_to_text_file('./diagonal_position_kill_heuristics.txt', result)

    def make_newly_applied_cell_heuristic_visited(self, heuristic_table, monitor_kill_heuristic_table, i, j):
        if i-1>-1 and j-1>-1 and self.board[i-1][j-1] != self.opponent_symbol:
            heuristic_table[i-1][j-1] = 1
            monitor_kill_heuristic_table[i-1][j-1] = True
        if i-1>-1 and j+1<self.board_size and self.board[i-1][j+1] != self.opponent_symbol:
            heuristic_table[i-1][j+1] = 1
            monitor_kill_heuristic_table[i-1][j+1] = True
        if i+1<self.board_size and j-1>-1 and self.board[i+1][j-1] != self.opponent_symbol:
            heuristic_table[i+1][j-1] = 1
            monitor_kill_heuristic_table[i+1][j-1] = True
        if i+1<self.board_size and j+1<self.board_size and self.board[i+1][j+1] != self.opponent_symbol:
            heuristic_table[i+1][j+1] = 1
            monitor_kill_heuristic_table[i+1][j+1] = True
        return (heuristic_table, monitor_kill_heuristic_table)

    def diagonal_position_reduce_cell_val(self):
        value_co_ordinates_list = list()
        monitor_kill_heuristic_table = list()
        heuristic_table = list()
        if os.path.isfile('./diagonal_position_kill_heuristics.txt'):
            result = self.read_from_json('./diagonal_position_kill_heuristics.txt')
            value_co_ordinates_list = result["value_co_ordinates_list"]
            monitor_kill_heuristic_table = result["monitor_kill_heuristic_table"]
            heuristic_table = result["heuristic_table"]
        else:
            for i in xrange(0, self.board_size):
                for j in xrange(0, self.board_size):
                    value_co_ordinates_list.append([self.cell_values[i][j], i, j])
                monitor_kill_heuristic_table.append([False] * self.board_size)
            value_co_ordinates_list = sorted(value_co_ordinates_list, key=itemgetter(0), reverse=True)
            heuristic_table = self.simple_matrix_copy(self.cell_values)
            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                        monitor_kill_heuristic_table, heuristic_table)
            

        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if monitor_kill_heuristic_table[i][j] and not self.possible_raids(i, j):
                    monitor_kill_heuristic_table[i][j] = False
                
        # Check if recent change of state can be taken as raid (Check this)
        if self.raid_kill():
            print "From kill strategy"
            return

        """
        # Two cases, next to my pawn
        changed_cordinates = self.get_prev_current_changed_coordinates()
        if changed_cordinates:
            for cordinate in changed_cordinates:
                i = cordinate[0]
                j = cordinate[1]
                if (i-1>-1 and self.board[i-1][j] == self.symbol) or \
                    (i+1<self.board_size and self.board[i+1][j] == self.symbol):
                    if (j-1>-1 and self.cell_values[i][j-1]) > (j+1<self.board_size and self.cell_values[i][j+1]):
                        if self.is_safe_against_next_raids(i, j-1) and self.board[i][j-1] == '.':
                            self.take_move(i, j-1)
                            heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                    heuristic_table, monitor_kill_heuristic_table,  i, j-1)
                            self.write_prev_state_output(self.board)
                            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                                monitor_kill_heuristic_table, heuristic_table)
                            print "Left or right securing 1"
                            return
                    else:
                        if self.is_safe_against_next_raids(i, j+1) and self.board[i][j+1] == '.':
                            self.take_move(i, j+1)
                            heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                    heuristic_table, monitor_kill_heuristic_table,  i, j+1)
                            self.write_prev_state_output(self.board)
                            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                                monitor_kill_heuristic_table, heuristic_table)
                            print "Left or right securing 2"
                            return
                if (j-1>-1 and self.board[i][j-1] == self.symbol) or \
                    (j+1<self.board_size and self.board[i][j+1] == self.symbol):
                    if (i-1>-1 and self.cell_values[i-1][j]) > (i+1<self.board_size and self.cell_values[i+1][j]):
                        if self.is_safe_against_next_raids(i-1, j) and self.board[i-1][j] == '.':
                            self.take_move(i-1, j)
                            heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                    heuristic_table, monitor_kill_heuristic_table,  i-1, j)
                            self.write_prev_state_output(self.board)
                            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                                monitor_kill_heuristic_table, heuristic_table)
                            print "Top or bottom securing 1"
                            return
                    else:
                        if self.is_safe_against_next_raids(i+1, j) and self.board[i+1][j] == '.':
                            self.take_move(i+1, j)
                            heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                    heuristic_table, monitor_kill_heuristic_table,  i+1, j)
                            self.write_prev_state_output(self.board)                    
                            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                                monitor_kill_heuristic_table, heuristic_table)                            
                            print "Top or bottom securing 2"
                            return

        """

        for index, val in enumerate(value_co_ordinates_list):
            i = val[1]
            j = val[2]
            # If the highest value pos is already occupied by opponent then leave it.
            if monitor_kill_heuristic_table[i][j] == True or \
                self.board[i][j] == self.opponent_symbol \
                or self.board[i][j] == self.symbol:                
                continue

            # If the highest value pos is safe against next rides, then take the highest position
            if self.is_safe_against_next_raids(i, j):
                if i-1>-1 and j-1>-1:
                    heuristic_table[i-1][j-1] = 1
                    monitor_kill_heuristic_table[i-1][j-1] = True
                if i-1>-1 and j+1<self.board_size:
                    heuristic_table[i-1][j+1] = 1
                    monitor_kill_heuristic_table[i-1][j+1] = True
                if i+1<self.board_size and j-1>-1:
                    heuristic_table[i+1][j-1] = 1
                    monitor_kill_heuristic_table[i+1][j-1] = True
                if i+1>self.board_size and j+1<self.board_size:
                    heuristic_table[i+1][j+1] = 1
                    monitor_kill_heuristic_table[i+1][j+1] = True

                self.take_move(i, j)
                heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                heuristic_table, monitor_kill_heuristic_table,  i, j)
                self.write_prev_state_output(self.board)
                self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                            monitor_kill_heuristic_table, heuristic_table)
                print "Taking highest possible piece"
                return 
            else:
                # If the highest value pos is not safe against next rides, then take the diagonal value.
                tmp_possible_list = list()
                print (val, i, j)
                if i-1>-1 and j-1>-1 and self.board[i-1][j-1] == "." \
                        and self.is_safe_against_next_raids(i-1, j-1):
                    tmp_possible_list.append([self.cell_values[i-1][j-1], i-1, j-1])
                if i-1>-1 and j+1<self.board_size and self.board[i-1][j+1] == "."\
                        and self.is_safe_against_next_raids(i-1, j+1):
                    tmp_possible_list.append([self.cell_values[i-1][j+1], i-1, j+1])
                if i+1<self.board_size and j-1>-1 and self.board[i+1][j-1] == "."\
                        and self.is_safe_against_next_raids(i+1, j-1):
                    tmp_possible_list.append([self.cell_values[i+1][j-1], i+1, j-1])
                if i+1<self.board_size and j+1<self.board_size and self.board[i+1][j+1] == "."\
                        and self.is_safe_against_next_raids(i+1, j+1):
                    tmp_possible_list.append([self.cell_values[i+1][j+1], i+1, j+1])

                print tmp_possible_list
                if tmp_possible_list:
                    tmp_possible_list = sorted(tmp_possible_list, key=itemgetter(0), reverse=True)
                    i = tmp_possible_list[0][1]
                    j = tmp_possible_list[0][2]
                    self.take_move(i, j)
                    heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                            heuristic_table, monitor_kill_heuristic_table,  i, j)
                    self.write_prev_state_output(self.board)
                    self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                            monitor_kill_heuristic_table, heuristic_table)
                    print "Securing highest possible piece"
                    return 


        os.system("touch stop_diagonal_position_strategy.txt")
        #raise Exception("Done with diagonal kill strategy")



    def execute_strategy(self):
        

        
        #raise Exception("Finished diagonal")
        total_chances = int(self.board_size * self.board_size/2)
        num_filled, num_unfilled = self.filled_unfilled_board_count()
        if num_filled < int(total_chances * 40/100):
            if not os.path.isfile('./stop_diagonal_position_strategy.txt'):
                self.diagonal_position_reduce_cell_val()
                print "Diagonal Positioning"
                return        
        
            else:
                if self.raid_kill():
                    print "Raid kill -> AB_1"
                    return
                alpha_beta_depth1 = AlphaBetaAlgo(self.symbol, 1,\
                                                  self.cell_values, self.board, self.board_size)
                action, move = alpha_beta_depth1.min_max_search()

                if self.is_safe_against_next_raids(action[0], action[1]):
                    alpha_beta_depth1.take_alphabeta_action(action, move)
                    print "Alpha Beta AB_1"
                else:
                    alpha_beta_depth2 = AlphaBetaAlgo(self.symbol, 2,\
                                                  self.cell_values, self.board, self.board_size)
                    action, move = alpha_beta_depth2.min_max_search()
                    alpha_beta_depth2.take_alphabeta_action(action, move)
                    print "Alpha Beta AB_2"

        elif num_filled < int(total_chances * 75/100):
            alpha_beta_depth2 = AlphaBetaAlgo(self.symbol, 2,\
                                          self.cell_values, self.board, self.board_size)
            action, move = alpha_beta_depth2.min_max_search()
            alpha_beta_depth2.take_alphabeta_action(action, move)
            print "Alpha Beta AB_2"
            return

        elif num_filled < int(total_chances * 90/100):
            alpha_beta_depth3 = AlphaBetaAlgo(self.symbol, 3,\
                                              self.cell_values, self.board, self.board_size)
            action, move = alpha_beta_depth3.min_max_search()
            alpha_beta_depth3.take_alphabeta_action(action, move)
            print "Alpha Beta AB_3"
            return
        else:
            alpha_beta_depth4 = AlphaBetaAlgo(self.symbol, 4,\
                                              self.cell_values, self.board, self.board_size)
            alpha_beta_depth4.min_max_search()
            action, move = alpha_beta_depth4.min_max_search()
            alpha_beta_depth4.take_alphabeta_action(action, move)
            print "Alpha Beta AB_4"
            return
        


                        

class GameServer(object):
    def __init__(object):
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
            for i in xrange(0, matrix_size):
                board_text = str(lines[i+1]).strip()
                row_val = list()
                for character in board_text:
                    row_val.append(character)
                board_state.append(row_val)
            return board_state

    def new_game(self):
        if os.path.isfile('./stop_boxing.txt'):
            os.system("\\rm -rf ./stop_boxing.txt")
        if os.path.isfile('./previous_state.txt'):
            os.system("\\rm -rf ./previous_state.txt")
        if os.path.isfile('./top_boxing_coordinates.txt'):
            os.system('\\rm -rf ./top_boxing_coordinates.txt')
        if os.path.isfile('./monitoring_kill_pos.txt'):
            os.system('\\rm -rf ./monitoring_kill_pos.txt')
        if os.path.isfile('./diagonal_position_kill_heuristics.txt'):
            os.system('\\rm -rf ./diagonal_position_kill_heuristics.txt')
        if os.path.isfile('./stop_diagonal_position_strategy.txt'):
            os.system('\\rm -rf ./stop_diagonal_position_strategy.txt')

            

    def start(self):
        read_input = ReadInput()
        read_input.read()
        board = read_input.board_state
        player_symbol = read_input.player_symbol
        matrix_size = read_input.matrix_size
        cell_values = read_input.cell_values
        count = 0
        opponent_symbol = 'X' if read_input.player_symbol == "O" else "O"
        self.new_game()


        opponent_time = 0
        my_time = 0

        
        print "Runing time: " + str() + " ms"

        while not self.is_game_over(board, matrix_size):
            read_input = ReadInput()
            read_input.read()
            
            start_time = time.time()
            print "Alpha Beta"
            minmax = AlphaBetaAlgo(opponent_symbol, read_input.depth,\
                                cell_values, board, read_input.matrix_size)
            (action, move) = minmax.min_max_search()
            minmax.take_alphabeta_action(action, move)
            opponent_time = opponent_time + int((time.time() - start_time) * 1000)


            print "======================"
            print "Clever Agent"
                   
            board = self.read_output(read_input.matrix_size)

            if self.is_game_over(board, matrix_size):
                score = self.get_score(board, read_input.matrix_size, player_symbol, opponent_symbol, cell_values)
                print "Stopping the game.... FUll"
                print "Score :", score
                print "Opponents Time:", opponent_time
                print "My Time:", my_time
                return

            start_time = time.time()
            strategy = AlternateBoxStrategy(read_input.matrix_size, board,\
                                        cell_values, player_symbol)
            strategy.execute_strategy()
            my_time = my_time + int((time.time() - start_time) * 1000)

            board = self.read_output(read_input.matrix_size)
            count = count + 1
            score = self.get_score(board, read_input.matrix_size, player_symbol, opponent_symbol, cell_values)
            print "Score :", score
            print "===================================================================="
        print "Opponents Time:", opponent_time
        print "My Time:", my_time

        

def main():
    read_input = ReadInput()
    read_input.read()
    
    print read_input.matrix_size
    print read_input.algo_type
    print read_input.player_symbol
    print read_input.depth
    print read_input.cell_values
    print read_input.board_state

    """
    if read_input.algo_type == "ALPHABETA":
        minmax = AlphaBetaAlgo(read_input.player_symbol, read_input.depth,\
                            read_input.cell_values, read_input.board_state, read_input.matrix_size)

        minmax.min_max_search()
    """
    game = GameServer()
    game.start()
    print "Finally"
    



if __name__ == "__main__":
    main()
