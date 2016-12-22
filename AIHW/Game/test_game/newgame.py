import os

def newgame():
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
	if os.path.isfile('./remaining_time.txt'):
	    os.system('\\rm -rf ./remaining_time.txt')
	if os.path.isfile('./calibration_error.txt'):
	    os.system('\\rm -rf ./calibration_error.txt')

#newgame()
