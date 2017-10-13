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
