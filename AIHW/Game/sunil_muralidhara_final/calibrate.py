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
        self._node_visted_count = 0

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

    @property
    def node_visted_count(self):
        return self._node_visted_count
    
    @node_visted_count.setter
    def node_visted_count(self, value):
        self._node_visted_count = value
    
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
        with open("calibrate_output.txt", "w") as fp:
            fp.write(move+'\n')
            for row in board:
                fp.write(''.join(row))
                fp.write('\n')

    def simple_matrix_copy(self, state):
        new_state = list()
        for i in xrange(0, self.board_size):
            new_state.append(['.']*self.board_size)
        for i in xrange(0, self.board_size):
            for j in xrange(0, self.board_size):
                new_state[i][j] = state[i][j]
        return new_state

    def min_max_search(self):
        v = self.max_value(self.board_state, -10000, 10000, self.depth)        
        move = self.alpha_num_mapping[self.best_col+1]+str(self.best_row+1)+" "+self.best_move_type
        action = [self.best_row, self.best_col, self.best_move_type, self.player_symbol]
        return (action, move)

    def take_alphabeta_action(self, action, move):
        new_board = self.new_state_based_on_action(self.board_state, action, self.player_symbol)
        self.print_board(new_board)
        self.write_to_output(move, new_board)
        
        
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
        self.node_visted_count = self.node_visted_count + 1
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
        self.node_visted_count = self.node_visted_count + 1
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

    def write_to_text_file(self, file_path, data):
        try:
            if data:
                with open(file_path, 'a') as fp:
                    fp.write(data)
                    fp.close()
        except:
            pass

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
        with open("calibrate_input.txt", "r") as fp:
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

    def simple_matrix_copy(self, state, board_size):
        new_state = list()
        for i in xrange(0, board_size):
            new_state.append(['.']*board_size)
        for i in xrange(0, board_size):
            for j in xrange(0, board_size):
                new_state[i][j] = state[i][j]
        return new_state

    def read_from_json(self, file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)

    def write_json_to_text_file(self, file_path, json_data):
        if json_data:
            with open(file_path, 'w') as fp:
                json.dump(json_data, fp)
                fp.close()

def calibrate():
    read_input = ReadInput()
    read_input.read()

    depth_find_dict = read_input.read_from_json("./depth_run_time_heuristics.txt")
    error_heuristic = dict()
    err_total = 0
    for i in xrange(2, 6):
        state = read_input.simple_matrix_copy(read_input.board_state, read_input.matrix_size)

        start_time = time.time()
        alphabeta = AlphaBetaAlgo(read_input.player_symbol, i,\
                            read_input.cell_values, state, read_input.matrix_size)

        # Total actions possible
        actions = alphabeta.possible_actions(read_input.board_state, read_input.player_symbol, "max_value")
        total_stake = 0
        total_raid = 0
        for j in actions:
            if j[2] == "Stake":
                total_stake = total_stake + 1
            else:
                total_raid = total_raid + 1

        (action, move) = alphabeta.min_max_search()
        alphabeta.take_alphabeta_action(action, move)
        
        depth = i
        total_time = int((time.time() - start_time) * 1000)
        total_action = total_stake + total_raid
        visited_nodes = alphabeta.node_visted_count


        theoritical_time = depth_find_dict[str(depth)][str(total_action)]
        error = float((theoritical_time - total_time)/(theoritical_time * 1.0))
        err_total = err_total + error
        error_heuristic[str(depth)] = error
        
        string_val = str(depth) + '|' + str(total_action) + '|' + str(total_time) + '|' \
             + str(total_stake) + '|' + str(total_raid) + '|' + str(read_input.matrix_size) + '|' + str(visited_nodes) +'\n'
        #print string_val,
    err_avg = err_total/4
    error_heuristic["6"] = err_avg
    error_heuristic["7"] = err_avg
    error_heuristic["8"] = err_avg
    error_heuristic["9"] = err_avg
    read_input.write_json_to_text_file("./calibration_error.txt", error_heuristic)
    #print error_heuristic
        
calibrate()
