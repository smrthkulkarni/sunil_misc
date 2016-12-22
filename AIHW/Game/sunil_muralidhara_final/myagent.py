from operator import itemgetter
import string
import os
import json
import time

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
            self._total_time = float(lines[3].strip()) * 1000 * 0.95

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
            #print ''.join(row)
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
        #self.print_board(new_board)
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

class AgentStrategy(object):
    def __init__(self, board_size, board, cell_values, symbol,\
                 remaining_time, remaining_moves, correction_time):
        self.board_size = board_size
        self.board = board 
        self.cell_values = cell_values
        self.symbol = symbol
        self.opponent_symbol = "X" if symbol == "O" else "O"
        self._alpha_num_mapping = self.get_alpha_num_dict()
        self.remaining_time = remaining_time
        self.remaining_moves = remaining_moves
        self.correction_time = correction_time

    @property
    def alpha_num_mapping(self):
        return self._alpha_num_mapping

    @alpha_num_mapping.setter
    def alpha_num_mapping(self, value):
        self._alpha_num_mapping = value

    def print_board(self, board):
        for row in board:
            #print ''.join(row)
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

    def read_from_json(self, file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def write_json_to_text_file(self, file_path, json_data):
        if json_data:
            with open(file_path, 'w') as fp:
                json.dump(json_data, fp)
                fp.close()

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

    def strategy_output(self, i, j, move_type, player_symbol):
        move = self.alpha_num_mapping[j+1]+str(i+1)+ " "+ move_type
        action = [i, j, move_type, player_symbol]
        new_board = self.new_state_based_on_action(self.board, action, player_symbol)
        #self.print_board(new_board)
        self.write_to_output(move, new_board)            

    def is_neighbours_unoccupied(self, i, j, board, symbol):
        if ((j-1 > -1) and (board[i][j-1] == symbol))\
            or ((j+1 < self.board_size) and (board[i][j+1] == symbol))\
            or ((i-1 > -1) and (board[i-1][j] == symbol))\
            or ((i+1 < self.board_size) and (board[i+1][j] == symbol)):
            return True
       

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
            #print i, j
            raise Exception("Not a valid move check")

        if self.is_neighbour(i, j, self.board, self.symbol) and\
           self.is_neighbour(i, j, self.board, self.opponent_symbol):
           self.strategy_output(i, j, "Raid", self.symbol)
           #print i, j, "Raid"
        else:
            self.strategy_output(i, j, "Stake", self.symbol)
            #print i, j, "Stake"

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

    def get_column_coordinates(self, j, y):
        if j-2 > -1 and y+2 < self.board_size:                        
            j = j - 2                        
            y = y + 2
        elif j-1 > -1 and j+3 < self.board_size:
            j = j - 1
            y = y + 3
        elif j == 0:
            y = y + 4
        elif y+1 < self.board_size:
            j = j - 3
            y = y + 1
        else:
            j = j - 4
        return j, y



    def raid_kill(self, value_co_ordinates_list, monitor_kill_heuristic_table, heuristic_table):
        raid_list = list()
        changed_cordinates = self.get_prev_current_changed_coordinates()
        #print "Changed cordinates ", changed_cordinates
        if changed_cordinates:
            for co_ordinates in changed_cordinates:
                raids = self.possible_raids(co_ordinates[0], co_ordinates[1])
                if raids:
                    raid_list.extend(raids)
                    break

        if raid_list:
            start_time = time.time()
            i = co_ordinates[0]
            j = co_ordinates[1]


            new_board = self.board
            new_cell_values = self.cell_values
            if self.board_size > 6:
                x = i
                y = j

                if i-2 > -1 and x+2 < self.board_size:
                    i = i - 2
                    x = x + 2
                    (j, y) = self.get_column_coordinates(j, y)

                elif i-1 > -1 and x+3 < self.board_size:
                    i = i - 1
                    x = x + 3
                    (j, y) = self.get_column_coordinates(j, y)

                elif i == 0:
                    x = x + 3
                    (j, y) = self.get_column_coordinates(j, y)
                
                elif x+1 < self.board_size:
                    i = i - 3
                    x = x + 1
                    (j, y) = self.get_column_coordinates(j, y)
                else:
                    i = i - 4
                    (j, y) = self.get_column_coordinates(j, y)

                new_board = list()
                new_cell_values = list()
                for m in xrange(i, x+1):
                    board_list = list()
                    cell_list = list()
                    for n in xrange(j, y+1):
                        #print self.board[m][n], 
                        board_list.append(self.board[m][n])
                        cell_list.append(self.cell_values[m][n])
                    #print 
                    new_board.append(board_list)
                    new_cell_values.append(cell_list)
            else:
                i = 0
                j = 0

            alpha_beta_depth2 = AlphaBetaAlgo(self.symbol, 5,\
                                              new_cell_values, new_board, len(new_board))
            action, move = alpha_beta_depth2.min_max_search()
           
            new_action = [action[0] + i, action[1] + j, action[2], action[3]]
            new_move = self.alpha_num_mapping[action[1] + j + 1]+str(action[0] + i + 1)+" "+action[2]

            

            alpha_beta_depth = AlphaBetaAlgo(self.symbol, 5,\
                                             self.cell_values, self.board, self.board_size)
            alpha_beta_depth.take_alphabeta_action(new_action, new_move)

            heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                                heuristic_table, monitor_kill_heuristic_table,  i, j)
            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                        monitor_kill_heuristic_table, heuristic_table)
            #print "Alpha beta 5: ", int((time.time() - start_time) * 1000)
            return True

        return False

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

    def possible_number_actions(self, board, symbol):
        # Possible stake moves
        stakes = list()
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if board[i][j] == ".":
                    stakes.append([i,j, 'Stake'])
        
        # Possible raid moves
        raids = list()
        for val in stakes:
            i = val[0]
            j = val[1]
            if self.is_neighbour(i, j, board, self.symbol) and self.is_neighbour(i, j, board, self.opponent_symbol):
                total_capture = self.find_total_captured_val(i, j, board, symbol)
                raids.append([i, j, 'Raid'])

        return len(raids) + len(stakes)

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
            
            for i in xrange(0, self.board_size):
                for j in xrange(0, self.board_size):
                    if self.board[i][j] == self.symbol:
                        heuristic_table, monitor_kill_heuristic_table = \
                            self.make_newly_applied_cell_heuristic_visited(heuristic_table,\
                                monitor_kill_heuristic_table, i, j)                        
            self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                        monitor_kill_heuristic_table, heuristic_table)

        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                if monitor_kill_heuristic_table[i][j] and not self.possible_raids(i, j):
                    monitor_kill_heuristic_table[i][j] = False

        # Check if recent change of state can be taken as raid (Check this)
        if self.raid_kill(value_co_ordinates_list, monitor_kill_heuristic_table, heuristic_table):
            #print "From kill strategy"
            return True

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
                self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                            monitor_kill_heuristic_table, heuristic_table)
                #print "Taking highest possible piece"
                return True
            else:
                # If the highest value pos is not safe against next rides, then take the diagonal value.
                tmp_possible_list = list()
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

                if tmp_possible_list:
                    tmp_possible_list = sorted(tmp_possible_list, key=itemgetter(0), reverse=True)
                    i = tmp_possible_list[0][1]
                    j = tmp_possible_list[0][2]
                    self.take_move(i, j)
                    heuristic_table, monitor_kill_heuristic_table = self.make_newly_applied_cell_heuristic_visited(\
                            heuristic_table, monitor_kill_heuristic_table,  i, j)
                    self.write_diagonal_position_kill_txt(value_co_ordinates_list,\
                            monitor_kill_heuristic_table, heuristic_table)
                    #print "Securing highest possible piece"
                    return True


        os.system("touch stop_diagonal_position_strategy.txt")

    def alpha_beta_depth_execution(self, depth, actions_len, depth_find_dict):
        depth = str(depth)
        theoritical_val = depth_find_dict[depth][str(actions_len)]
        corrected_time = theoritical_val - (theoritical_val * float(self.correction_time[depth]))
        #print depth, actions_len, corrected_time, theoritical_val, self.correction_time[depth]
        #print "Remaining time/move ", self.remaining_time/(self.remaining_moves), self.remaining_time, self.remaining_moves
        if (self.remaining_time/(self.remaining_moves) > (corrected_time * 1.05)):
            alpha_beta_depth = AlphaBetaAlgo(self.symbol, int(depth),\
                                             self.cell_values, self.board, self.board_size)
            action, move = alpha_beta_depth.min_max_search()
            alpha_beta_depth.take_alphabeta_action(action, move)
            #print "Alpha Beta "+ depth
            return True
        else:
            return False

    def execute_strategy(self):
        #raise Exception("Finished diagonal")
        total_chances = int(self.board_size * self.board_size/2)
        ##print "&&&&&&&&&&&&&&&&&&&&&&&&"
        ##print total_chances, self.remaining_moves
        ##print int(total_chances * 40/100)
        ##print total_chances - self.remaining_moves
        ##print "&&&&&&&&&&&&&&&&&&&&&&&&"


        # Check if the depth 4 perform this
        actions_len = self.possible_number_actions(self.board, self.symbol)        
        depth_find_dict = self.read_from_json("./depth_run_time_heuristics.txt")
        do_diagonal_position_strategy = True
        
        start_time = time.time()
        if not os.path.isfile('./stop_diagonal_position_strategy.txt'):
            if (str(actions_len) in depth_find_dict[str(4)]):
                theoritical_val = float(depth_find_dict[str(4)][str(actions_len)])
                corrected_time = theoritical_val - (theoritical_val * float(self.correction_time["4"]))
                if (self.remaining_time/(self.remaining_moves) > (corrected_time * 1.05)):
                    #print "Stoping the stupid diagonal position strategy"
                    do_diagonal_position_strategy = False
            
            if do_diagonal_position_strategy:
                if (total_chances - self.remaining_moves) < int(total_chances * 35/100):
                    if self.diagonal_position_reduce_cell_val():
                        #print "Diagonal Positioning"
                        #print "time depth: ", int((time.time() - start_time) * 1000)
                        self.write_prev_state_output(self.board)
                        return
            os.system("touch stop_diagonal_position_strategy.txt")
        
        
            # Total actions possible
            
            
            ##print "&&&&&&&&&&&&&&&&&&&&&&&&"
            ##print "Action len", actions_len
            ##print "Remaining time", self.remaining_time
            ##print "self.remaining_moves", self.remaining_moves
            ##print "depth_find_dict[4][str(actions_len)]", depth_find_dict["4"][str(actions_len)]
            ##print "depth_find_dict[3][str(actions_len)]",depth_find_dict["3"][str(actions_len)]
            ##print "depth_find_dict[2][str(actions_len)]",depth_find_dict["2"][str(actions_len)]
            ##print "self.remaining_time/self.remaining_moves ", self.remaining_time/self.remaining_moves
            ##print "&&&&&&&&&&&&&&&&&&&&&&&&"
        start_time = time.time()        
        for i in xrange(9, 1, -1):
            if str(actions_len) in depth_find_dict[str(i)]:
                if self.alpha_beta_depth_execution(i, actions_len, depth_find_dict):
                    #print "Alpha beta strategy No.: ", i
                    #print "Time taken: ", int((time.time() - start_time) * 1000)
                    self.write_prev_state_output(self.board)
                    return
        
            

        #raise Exception("Didnt satify any strategy condition check....")

        start_time = time.time()  
        alpha_beta_depth2 = AlphaBetaAlgo(self.symbol, 2,\
                                          self.cell_values, self.board, self.board_size)
        action, move = alpha_beta_depth2.min_max_search()
        alpha_beta_depth2.take_alphabeta_action(action, move)
        self.write_prev_state_output(self.board)
        #print "Alpha beta 2: ", int((time.time() - start_time) * 1000)

        #print "Alpha Beta AB_2"
        return

            
def run():
    start_time = time.time()
    read_input = ReadInput()
    read_input.read()
    
    ##print read_input.matrix_size
    ##print read_input.algo_type
    ##print read_input.player_symbol
    ##print read_input.total_time
    ##print read_input.cell_values
    ##print read_input.board_state

    remaining_time = read_input.total_time
    remaining_moves = 0

    # Gives the correction for each depth
    correction_time = read_input.read_from_json("./calibration_error.txt")

    if os.path.isfile('./remaining_time.txt'):
        result = read_input.read_from_json("./remaining_time.txt")
        remaining_time = result[0]
        remaining_moves = result[1] - 1
    else:
        for i in xrange(0, read_input.matrix_size):
            for j in xrange(0, read_input.matrix_size):
                if read_input.board_state[i][j] == '.':
                    remaining_moves = remaining_moves + 1
        remaining_moves = (remaining_moves/2) if remaining_moves % 2 == 0 else (remaining_moves/2) + 1

    
    strategy = AgentStrategy(read_input.matrix_size, read_input.board_state, read_input.cell_values,\
                             read_input.player_symbol, remaining_time, remaining_moves, correction_time)
    strategy.execute_strategy()
    my_time = int((time.time() - start_time) * 1000)
    remaining_time = remaining_time - my_time
    read_input.write_json_to_text_file("./remaining_time.txt", [remaining_time, remaining_moves])

run()