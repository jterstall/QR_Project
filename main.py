import State

# variables = ['Inflow', 'Volume', 'Outflow']
def init_values():
	magnitude = [[0, 1], [0, 1, 2], [0, 1, 2]]
	derivatives = [-1, 0, 1]
	# First index: magnitude, Second index: derivative
	inflow_new_matrix = [[0, 1, "Not Possible"], [1, 1, [0, 1]]]
	
	# First index magnitude inflow, second index magnitude outflow, third index derivative volume
	vol_der_matrix = [[0, -1, -1], [1, [[1, 0, -1], [1, 0], [-1, 0]], [[1, 0, -1], [1, 0], [-1, 0]]]]
	
	# First index magnitude volume, second index derivative volume
	vol_new_matrix = [[0, [0, 1], "Not Possible"], [1, [1, 2], [1, 0]], [2, "Not Possibru", 1]]

	begin_state = State.State([0, 0], [0, 0], [0, 0])

	return begin_state, magnitude, derivatives, inflow_new_matrix, vol_der_matrix, vol_new_matrix

def find_valid_successor_states(state, derivatives, variables):
	successor_states = []
	return successor_states

def get_possible_inflow(state, inflow_new_matrix):
	states = []
	new_inflow_value = inflow_new_matrix[state.inflow[0]][state.inflow[1]]
	if isinstance(new_inflow_value, str):
		return states
	if isinstance(new_inflow_value, list):
		for value in new_inflow_value:
			states.append(State.State([value, state.inflow[1]], state.volume, state.outflow))
	else:
		states.append(State.State([new_inflow_value, state.inflow[1]], state.volume, state.outflow))
	return states

def get_possible_volume_derivatives(state, vol_der_matrix):
	states = []
	if state.inflow[0] > 0 and state.outflow[0] > 0:
		new_vol_der = vol_der_matrix[state.inflow[0]][state.outflow[0]][state.volume[1]]
	else:
		new_vol_der = vol_der_matrix[state.inflow[0]][state.outflow[0]]
	if isinstance(new_vol_der, list):
		for der in new_vol_der:
			states.append(State.State(state.inflow, [state.volume[0], der], [state.outflow[0], der]))
	else:
		states.append(State.State(state.inflow, [state.volume[0], new_vol_der], [state.outflow[0], new_vol_der]))
	return states

def get_possible_volume(state, vol_new_matrix):
	states = []
	new_vol = vol_new_matrix[state.volume[0]][state.volume[1]]
	if isinstance(new_vol, str):
		return states
	if isinstance(new_vol, list):
		for vol in new_vol:
			states.append(State.State(state.inflow, [vol, state.volume[1]], [vol, state.outflow[1]]))
	else:
		states.append(State.State(state.inflow, [new_vol, state.volume[1]], [new_vol, state.outflow[1]]))
	return states

def main():
	begin_state, magnitude, derivatives, inflow_new_matrix, vol_der_matrix, vol_new_matrix = init_values()
	
	possible_inflow_new = get_possible_inflow(begin_state, inflow_new_matrix)
	possible_vol_der_new = get_possible_volume_derivatives(begin_state, vol_der_matrix)
	possible_vol_new = get_possible_volume(begin_state, vol_new_matrix)
	
	for state in possible_vol_new:
		state.pretty_print()
		print("")

	states_to_explore = [begin_state]
	already_visited = [begin_state]
	succesor_states = []
	# while not empty(states_to_explore):
	# 	for state in states_to_explore:
	# 		already_visited.append(state)
	# 		succesor_states = find_valid_successor_states(state, derivatives, variables)
	# 	successor_states.append(children)
	# 	states_to_explore = []
	# 	if not in already_visited:
	# 		states_to_explore.append(children[i])

if __name__ == '__main__':
	main()