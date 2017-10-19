class State:
	# Row 1 means inflow set to 1. Effect on inflow, volume, outflow respectively

	def __init__(self, inflow, volume, outflow, height, pressure):
		self.inflow = inflow
		self.volume = volume
		self.outflow = outflow
		self.height = height
		self.pressure = pressure

	def pretty_print(self):
		print("Inflow: {0}".format(self.inflow))
		print("Volume: {0}".format(self.volume))
		print("Outflow: {0}".format(self.outflow))
		print("Height: {0}".format(self.volume))
		print("Pressure: {0}".format(self.outflow))
		print("")

	def rip(self):
		return "State.State({0}, {1}, {2})".format(self.inflow, self.volume, self.outflow)

	def create_label(self):
		return "[" + str(self.inflow) + "," + str(self.volume) + "," + str(self.outflow) + "," + str(self.height) + "," + str(self.pressure) + "]"

	def compare_state(self, other_state):
		return self.inflow == other_state.inflow and self.outflow == other_state.outflow and self.volume == other_state.volume \
			and self.height == other_state.height and self.pressure == other_state.pressure

		
	def differences(self, other_state):
		return [self.inflow[0] == other_state.inflow[0], self.inflow[1] == other_state.inflow[1], self.volume[0] == other_state.volume[0], self.volume[1] == other_state.volume[1]]
