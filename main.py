from collections import Counter
import ast
import State
import itertools
import networkx as nx
import state_matrices
import matplotlib.pyplot as plt

# Authors: Jeroen Terstall, Tycho Koster
# This file handles the main algorithm that models the behavior of a sink/bath.


# Retrieve all possible transitions by changing the inflow of a state
def get_possible_inflow(state):
	states = []

	# Retrieve possible new inflow values by retrieving it from the new inflow matrix
	new_inflow_value = state_matrices.inflow_new_matrix[state.inflow[0]][state.inflow[1]]

	# If not possible, just return an empty list
	if isinstance(new_inflow_value, str):
		return states
	# If multiple possible values create all possible new states and add to the list
	elif isinstance(new_inflow_value, list):
		for value in new_inflow_value:
			# Prevent impossible value with magnitude 0 and derivative -1
			if value == 0 and state.inflow[1] == -1:
				states.append(State.State([value, 0], state.volume, state.outflow, state.height, state.pressure))
			else:
				states.append(State.State([value, state.inflow[1]], state.volume, state.outflow, state.height, state.pressure))
	# If only one possible value, create that state and return it
	else:
		states.append(State.State([new_inflow_value, state.inflow[1]], state.volume, state.outflow, state.height, state.pressure))

	return states

# Retrieve all possible transitions by changing the derivative of the volume
def get_possible_volume_derivatives(state):
	states = []

	# If the outflow and inflow > 0, then the volume derivative needs to be used to determine the new derivative
	if state.inflow[0] > 0 and state.outflow[0] > 0:
		new_vol_der = state_matrices.vol_der_matrix[state.inflow[0]][state.outflow[0]][state.volume[1]]
	# If not, outflow and inflow are sufficient
	else:
		new_vol_der = state_matrices.vol_der_matrix[state.inflow[0]][state.outflow[0]]

	# If multiple possible values possible, create states with all of them
	if isinstance(new_vol_der, list):
		for der in new_vol_der:
			states.append(State.State(state.inflow, [state.volume[0], der], [state.outflow[0], der], [state.height[0], der], [state.pressure[0], der]))
	# If not, just one state
	else:
		states.append(State.State(state.inflow, [state.volume[0], new_vol_der], [state.outflow[0], new_vol_der], [state.height[0], new_vol_der], [state.pressure[0], new_vol_der]))

	return states

# Retrieve all possible transitions by changing the magnitude of the volume
def get_possible_volume(state):
	states = []

	# Retrieve possible new value(s) from the matrix
	new_vol = state_matrices.vol_new_matrix[state.volume[0]][state.volume[1]]
	
	# If no possible values
	if isinstance(new_vol, str):
		return states
	# If multiple possible values, add them all
	elif isinstance(new_vol, list):
		for vol in new_vol:
			# Prevent impossible states with magnitude 0, 2 and derivative 1, -1 respectively
			if (vol == 2 and state.volume[1] == 1) or (vol == 0 and state.volume[1] == -1):
				states.append(State.State(state.inflow, [vol, 0], [vol, 0], [vol, 0], [vol, 0]))
			else:
				states.append(State.State(state.inflow, [vol, state.volume[1]], [vol, state.outflow[1]], [vol, state.height[1]], [vol, state.pressure[1]]))
	# Ìf only one possibility, create that state
	else:
		if (new_vol == 2 and state.volume[1] == 1) or (new_vol == 0 and state.volume[1] == -1):
			states.append(State.State(state.inflow, [new_vol, 0], [new_vol, 0], [new_vol, 0], [new_vol, 0]))
		else:
			states.append(State.State(state.inflow, [new_vol, state.volume[1]], [new_vol, state.outflow[1]], [new_vol, state.height[1]], [new_vol, state.pressure[1]]))
	return states

# Function that manually changes the inflow derivative
def change_inflow(state, visited):
	new_states = []

	# Retrieve possible new inflow derivatives
	new_derivatives = state_matrices.inflow_der_matrix[state.inflow[1]][state.inflow[0]]

	# If more than one possibility, create all states
	if isinstance(new_derivatives, list):
		for derivative in new_derivatives:
			new_state = State.State([state.inflow[0], derivative], state.volume, state.outflow, state.height, state.pressure)
			# Check if the state was already visited once. If not, add to exploration list
			equal_states = [new_state.compare_state(visited_state) for visited_state in visited]
			if not any(equal_states):
				new_states.append(new_state)
	# If not, create one state
	else:
		new_state = State.State([state.inflow[0], new_derivatives], state.volume, state.outflow, state.height, state.pressure)
		# Check if the state was already visited once. If not, add to exploration list
		equal_states = [new_state.compare_state(visited_state) for visited_state in visited]
		if not any(equal_states):
			new_states.append(new_state)

	return new_states

# Function that generates all successor states based on the current value that is being changed.
# Additionally, adds the nodes and edges to the state graph
# Returns all successor states of a certain state and the current version of the state graph
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

# Function to check if a state has already been visited
def check_visited(successor_states, visited, states_to_explore, G):
	changed = []
	old_states_to_explore = list(states_to_explore)
	states_to_explore = []
	for state in successor_states:
		# Check all successor states for visited status, if not add to states to explore
		equal_states = [state.compare_state(visited_state) for visited_state in visited]
		if not any(equal_states):
			states_to_explore.append(state)
			visited.append(state)
		# If all successor states are visited, manually change the derivative of the inflow
		else:
			changed_inflow_states = change_inflow(state, visited)
			# Also add changed state to the state graph
			for changed_inflow_state in changed_inflow_states:
				G.add_node(changed_inflow_state.create_label())
				G.add_edge(state.create_label(), changed_inflow_state.create_label())
				changed.append(changed_inflow_state)
				visited.append(changed_inflow_state)
	return old_states_to_explore, states_to_explore, visited, changed, G

# Function that displays the state graph
def show_graph(G):
	plt.figure(figsize = (9, 9))
	print("Number of states: {0}".format(len(G)))

	# # Uncomment to get the nodes that correspond to its index
	# nodes = G.nodes()
	# for i in range(len(nodes)):
	# 	print(i)
	# 	print(nodes[i])

	G = nx.convert_node_labels_to_integers(G)

	colors = ['red', 'yellow', 'cyan', 'pink', 'orange', 'violet']
	pos = nx.spring_layout(G)
	nodes = nx.draw_networkx_nodes(G, pos, node_size = 500, node_color=colors)
	nodes.set_edgecolor('black')
	nx.draw_networkx_labels(G, pos)
	nx.draw_networkx_edges(G, pos, arrows=True, style='dashdot')
	plt.show()

# Function that prints the kind of transition made between states.
def print_transition(state, other_state):
	# Check where the two states differ
	differences = state.differences(other_state)

	# Display message based on where the difference is
	if not differences[0]:
		print("Can transition to the following state because the inflow magnitude changes from {0} to {1}".format(state.inflow[0], other_state.inflow[0]))
	elif not differences[1]:
		print("Can transition to the following state by setting the inflow derivative from {0} to {1}".format(state.inflow[1], other_state.inflow[1]))
	elif not differences[2]:
		print("Can transition to the following state because the volume magnitude changes from {0} to {1}".format(state.volume[0], other_state.volume[0]))
	elif not differences[3]:
		print("Can transition to the following state because the volume derivative changes from {0} to {1}".format(state.volume[1], other_state.volume[1]))


# Function that prints the trace, with the steps the algorithm takes
def print_state_transitions(G):
	for edge in G.edges():
		# Dont display a transition that goes to itself
		if not edge[0] == edge[1]:
			# Literally evaluate the state label to get the state values
			begin_state = ast.literal_eval(edge[0])
			end_state = ast.literal_eval(edge[1])
			# Print the transition
			print("State:")
			begin_state_obj = State.State(begin_state[0], begin_state[1], begin_state[2], begin_state[3], begin_state[4])
			begin_state_obj.pretty_print()
			end_state_obj = State.State(end_state[0], end_state[1], end_state[2], end_state[3], end_state[4])
			print_transition(begin_state_obj, end_state_obj)
			end_state_obj.pretty_print()

# Function that does all the work
# Calls all the steps in the algorithm
def generate_state_graph(begin_states):
	G = nx.DiGraph()

	for begin_state in begin_states:

		# Instantiate the begin state as already visited and to be explored
		visited = [begin_state]
		states_to_explore = [begin_state]
		successor_states = []

		while states_to_explore:
			# First change the inflow magnitude based on inflow derivative
			successor_states, G = generate_successor_states("Inflow", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_inflow, G = check_visited(successor_states, visited, states_to_explore, G)

			# If no possible non-visited states were generated above, the inflow derivative was manually changed and the code below is run
			# Handles special case where the volume needed to be changed before the volume derivative
			if changed_inflow:
				successor_states, G = generate_successor_states("Volume", old_states_to_explore, G)
				_, states_to_explore, visited, _, G = \
					check_visited(successor_states, visited, states_to_explore, G)

			# Transitions based on the volume derivative 
			successor_states, G = generate_successor_states("Vol-Der", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_vol_der, G = check_visited(successor_states, visited, states_to_explore, G)

			# Transitions based on the volume magnitude
			successor_states, G = generate_successor_states("Volume", states_to_explore, G)
			old_states_to_explore, states_to_explore, visited, changed_vol, G = check_visited(successor_states, visited, states_to_explore, G)

			# If any states with changed inflow derivatives exist that were not visited yet, add them to the states to explore for next iteration
			for changed_state in changed_inflow:
				states_to_explore.append(changed_state)
			for changed_state in changed_vol_der:
				states_to_explore.append(changed_state)
			for changed_state in changed_vol:
				states_to_explore.append(changed_state)

	return G, visited


def main():
	# Retrieve visited states and stategraph for a single run through with begin state containing all zeros
	G, visited = generate_state_graph(state_matrices.begin_state)
	
	# Trace
	print_state_transitions(G)

	# Generate rest of states and edges
	G, _ = generate_state_graph(visited)

	show_graph(G)

if __name__ == '__main__':
	main()

