class State:
	# Row 1 means inflow set to 1. Effect on inflow, volume, outflow respectively

	def __init__(self, inflow, volume, outflow):
		self.inflow = inflow
		self.volume = volume
		self.outflow = outflow

	def pretty_print(self):
		print("Inflow: {0}".format(self.inflow))
		print("Volume: {0}".format(self.volume))
		print("Outflow: {0}".format(self.outflow))
		print("")

	def rip(self):
		return "State.State({0}, {1}, {2})".format(self.inflow, self.volume, self.outflow)

	def create_label(self):
		return str(self.inflow) + str(self.volume) + str(self.outflow)

	def compare_state(self, state):
		return self.inflow == state.inflow and self.outflow == state.outflow and self.volume == state.volume
