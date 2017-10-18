from collections import Counter
import State
import itertools
import networkx as nx
import state_matrices
import matplotlib.pyplot as plt

def get_possible_inflow(state):
	states = []
	new_inflow_value = state_matrices.inflow_new_matrix[state.inflow[0]][state.inflow[1]]
	if isinstance(new_inflow_value, str):
		return states
	elif isinstance(new_inflow_value, list):
		for value in new_inflow_value:
			if value == 0 and state.inflow[1] == -1:
				states.append(State.State([value, 0], state.volume, state.outflow))
			else:
				states.append(State.State([value, state.inflow[1]], state.volume, state.outflow))
	else:
		states.append(State.State([new_inflow_value, state.inflow[1]], state.volume, state.outflow))
	return states


def get_possible_volume_derivatives(state):
	states = []
	if state.inflow[0] > 0 and state.outflow[0] > 0:
		new_vol_der = state_matrices.vol_der_matrix[state.inflow[0]][state.outflow[0]][state.volume[1]]
	else:
		new_vol_der = state_matrices.vol_der_matrix[state.inflow[0]][state.outflow[0]]
	if isinstance(new_vol_der, list):
		for der in new_vol_der:
			states.append(State.State(state.inflow, [state.volume[0], der], [state.outflow[0], der]))
	else:
		states.append(State.State(state.inflow, [state.volume[0], new_vol_der], [state.outflow[0], new_vol_der]))
	return states


def get_possible_volume(state):
	states = []
	new_vol = state_matrices.vol_new_matrix[state.volume[0]][state.volume[1]]
	if isinstance(new_vol, str):
		return states
	elif isinstance(new_vol, list):
		for vol in new_vol:
			if (vol == 2 and state.volume[1] == 1) or (vol == 0 and state.volume[1] == -1):
				states.append(State.State(state.inflow, [vol, 0], [vol, 0]))
			else:
				states.append(State.State(state.inflow, [vol, state.volume[1]], [vol, state.outflow[1]]))

	else:
		if (new_vol == 2 and state.volume[1] == 1) or (new_vol == 0 and state.volume[1] == -1):
			states.append(State.State(state.inflow, [new_vol, 0], [new_vol, 0]))
		else:
			states.append(State.State(state.inflow, [new_vol, state.volume[1]], [new_vol, state.outflow[1]]))
	return states


def change_inflow(state, visited):
	new_states = []
	new_derivatives = state_matrices.inflow_der_matrix[state.inflow[1]][state.inflow[0]]
	if isinstance(new_derivatives, list):
		for derivative in new_derivatives:
			new_state = State.State([state.inflow[0], derivative], state.volume, state.outflow)
			equal_states = [new_state.compare_state(visited_state) for visited_state in visited]
			if not any(equal_states):
				new_states.append(new_state)
	else:
		new_state = State.State([state.inflow[0], new_derivatives], state.volume, state.outflow)
		equal_states = [new_state.compare_state(visited_state) for visited_state in visited]
		if not any(equal_states):
			new_states.append(new_state)
	return new_states


def generate_successor_states(identifier, states_to_explore, G):
	successor_states = []
	if identifier == "Inflow":
		for state in states_to_explore:
			G.add_node(state.create_label())
			possible_states = get_possible_inflow(state)
			for possible_state in possible_states:
				successor_states.append(possible_state)
				G.add_node(possible_state.create_label())
				G.add_edge(state.create_label(), possible_state.create_label())
	elif identifier == "Vol-Der":
		for state in states_to_explore:
			G.add_node(state.create_label())
			possible_states = get_possible_volume_derivatives(state)
			for possible_state in possible_states:
				successor_states.append(possible_state)
				G.add_node(possible_state.create_label())
				G.add_edge(state.create_label(), possible_state.create_label())
	elif identifier == "Volume":
		for state in states_to_explore:
			G.add_node(state.create_label())
			possible_states = get_possible_volume(state)
			for possible_state in possible_states:
				successor_states.append(possible_state)
				G.add_node(possible_state.create_label())
				G.add_edge(state.create_label(), possible_state.create_label())
	return successor_states, G


def check_visited(successor_states, visited, states_to_explore, G):
	changed = []
	old_states_to_explore = list(states_to_explore)
	states_to_explore = []
	for state in successor_states:
		equal_states = [state.compare_state(visited_state) for visited_state in visited]
		if not any(equal_states):
			states_to_explore.append(state)
			visited.append(state)
		else:
			changed_inflow_states = change_inflow(state, visited)
			for changed_inflow_state in changed_inflow_states:
				G.add_node(changed_inflow_state.create_label())
				G.add_edge(state.create_label(), changed_inflow_state.create_label())
				changed.append(changed_inflow_state)
				visited.append(changed_inflow_state)
	return old_states_to_explore, states_to_explore, visited, changed, G

def show_graph(G):
	plt.figure(figsize = (9, 9))

	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, node_size = 500)
	nx.draw_networkx_labels(G, pos)
	nx.draw_networkx_edges(G, pos, arrows=True)
	plt.show()


def generate_state_graph(begin_states):
	G = nx.DiGraph()

	for begin_state in begin_states:

		visited = [begin_state]
		states_to_explore = [begin_state]
		successor_states = []

		while states_to_explore:
			print("DEJA VU, I HAVE BEEN IN THIS PLACE BEFORE")

			successor_states, G = generate_successor_states("Inflow", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_inflow, G = check_visited(successor_states, visited, states_to_explore, G)

			# Changed leeg gooien?
			if changed_inflow:
				successor_states, G = generate_successor_states("Volume", old_states_to_explore, G)
				_, states_to_explore, visited, _, G = check_visited(successor_states, visited, states_to_explore, G)

			successor_states, G = generate_successor_states("Vol-Der", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_vol_der, G = check_visited(successor_states, visited, states_to_explore, G)

			successor_states, G = generate_successor_states("Volume", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_vol, G = check_visited(successor_states, visited, states_to_explore, G)

			for changed_state in changed_inflow:
				states_to_explore.append(changed_state)
			for changed_state in changed_vol_der:
				states_to_explore.append(changed_state)
			for changed_state in changed_vol:
				states_to_explore.append(changed_state)
	return G, visited


def main():
	G, visited = generate_state_graph(state_matrices.begin_state)
	G, _ = generate_state_graph(visited)
	print(len(G))
	show_graph(G)

if __name__ == '__main__':
	main()