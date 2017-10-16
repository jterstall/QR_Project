from collections import Counter
import State
import networkx as nx
import matplotlib.pyplot as plt

# variables = ['Inflow', 'Volume', 'Outflow']
def init_values():
	magnitude = [[0, 1], [0, 1, 2], [0, 1, 2]]
	derivatives = [-1, 0, 1]
	# First index: magnitude, Second index: derivative
	inflow_new_matrix = [[0, 1, "Not Possible"], [1, 1, [0, 1]]]
	
	# First index magnitude inflow, second index magnitude outflow, third index derivative volume
	vol_der_matrix = [[0, -1, -1], [1, [[1, 0, -1], [1, 0], [-1, 0]], [[0, -1], [1, 0], [-1, 0]]]]
	
	# First index magnitude volume, second index derivative volume
	vol_new_matrix = [[0, [0, 1], "Not Possible"], [1, [1, 2], [1, 0]], [2, "Not Possibru", 1]]

	begin_state = State.State([0, 0], [0, 0], [0, 0])

	return begin_state, magnitude, derivatives, inflow_new_matrix, vol_der_matrix, vol_new_matrix

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
			if vol == 2 and state.volume[1] == 1:
				states.append(State.State(state.inflow, [vol, 0], [vol, 0]))
			else:
				states.append(State.State(state.inflow, [vol, state.volume[1]], [vol, state.outflow[1]]))

	else:
		if new_vol == 2 and state.volume[1] == 1:
			states.append(State.State(state.inflow, [new_vol, 0], [new_vol, 0]))
		else:
			states.append(State.State(state.inflow, [new_vol, state.volume[1]], [new_vol, state.outflow[1]]))
	return states

def change_inflow(state, already_visited, derivatives):
	new_states = []
	for derivative in derivatives:
		new_state = State.State([state.inflow[0], derivative], state.volume, state.outflow)
		visited = [new_state.compare_state(visited_state) for visited_state in already_visited]
		if not any(visited):
			new_states.append(new_state)
	return new_states


def generate_successor_states(identifier, matrix, states_to_explore):
	successor_states = []
	if identifier == "Inflow":
		for state in states_to_explore:
			possible_states = get_possible_inflow(state, matrix)
			for possible_state in possible_states:
				successor_states.append(possible_state)
	elif identifier == "Vol-Der":
		for state in states_to_explore:
			possible_states = get_possible_volume_derivatives(state, matrix)
			for possible_state in possible_states:
				successor_states.append(possible_state)
	elif identifier == "Volume":
		for state in states_to_explore:
			possible_states = get_possible_volume(state, matrix)
			for possible_state in possible_states:
				successor_states.append(possible_state)
	return successor_states

def check_visited(successor_states, already_visited, states_to_explore, derivatives):
	changed = []
	for state in successor_states:
		visited = [state.compare_state(visited_state) for visited_state in already_visited]
		if not any(visited):
			states_to_explore.append(state)
			already_visited.append(state)
		else:
			changed_inflow_states = change_inflow(state, already_visited, derivatives)
			for changed_inflow_state in changed_inflow_states:
				changed.append(changed_inflow_state)
				already_visited.append(changed_inflow_state)
	return states_to_explore, already_visited, changed

def main():
	begin_state, magnitude, derivatives, inflow_new_matrix, vol_der_matrix, vol_new_matrix = init_values()

	states_to_explore = [begin_state]
	already_visited = [begin_state]
	successor_states = []
	
	while states_to_explore:
		print("DEJA VU, I HAVE BEEN IN THIS PLACE BEFORE")
		successor_states = generate_successor_states("Inflow", inflow_new_matrix, states_to_explore)
		states_to_explore = []
		states_to_explore, already_visited, changed = check_visited(successor_states, already_visited, states_to_explore, derivatives)
		

		successor_states = generate_successor_states("Vol-Der", vol_der_matrix, states_to_explore)
		states_to_explore = []
		states_to_explore, already_visited, changed_1 = check_visited(successor_states, already_visited, states_to_explore, derivatives)

		successor_states = generate_successor_states("Volume", vol_new_matrix, states_to_explore)
		states_to_explore = []
		states_to_explore, already_visited, changed_2 = check_visited(successor_states, already_visited, states_to_explore, derivatives)

		for changed_state in changed:
			states_to_explore.append(changed_state)
		for changed_state in changed_1:
			states_to_explore.append(changed_state)
		for changed_state in changed_2:
			states_to_explore.append(changed_state)


	plt.figure(figsize = (13, 13))

	G = nx.DiGraph()

	for i in range(len(already_visited)):
		G.add_node(i)

	successor_states = []
	for i, state in enumerate(already_visited):
		successor_states.append(generate_successor_states("Inflow", inflow_new_matrix, [state]))
		successor_states.append(generate_successor_states("Vol-Der", vol_der_matrix, [state]))
		successor_states.append(generate_successor_states("Volume", vol_new_matrix, [state]))
		successor_list = [successor_state for sublist in successor_states for successor_state in sublist]
		for j, other_state in enumerate(already_visited):
			for successor_state in successor_list:
				if(other_state.compare_state(successor_state)):
					G.add_edge(i, j)
					# state.pretty_print()
					# other_state.pretty_print()
					# print("END")
					break

	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, node_size = 500)
	nx.draw_networkx_labels(G, pos)
	nx.draw_networkx_edges(G, pos, arrows=True)
	plt.show()

if __name__ == '__main__':
	main()