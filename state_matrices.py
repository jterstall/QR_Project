import State

inflow_magnitude = [0, 1]
outflow_magnitude = [0, 1, 2]
volume_magnitude = [0, 1, 2]

magnitude = [[0, 1], [0, 1, 2], [0, 1, 2]]
derivatives = [-1, 0, 1]

 # First index = old derivative inflow, second index = inflow value
inflow_der_matrix = [[1, [-1, 1]], [0, 0], [0, 0]]

# First index: magnitude, Second index: derivative
inflow_new_matrix = [[0, 1, "Not Possible"], [1, 1, [0, 1]]]
	
# First index magnitude inflow, second index magnitude outflow, third index derivative volume
vol_der_matrix = [[0, -1, -1], [1, [[1, 0, -1], [1, 0], [-1, 0]], [[0, -1], [1, 0], [-1, 0]]]]
	
# First index magnitude volume, second index derivative volume
vol_new_matrix = [[0, [0, 1], "Not Possible"], [1, [1, 2], [1, 0]], [2, "Not Possibru", 1]]

begin_state = [State.State([0, 0], [0, 0], [0, 0])]