import os
import pwd

'''
s1
s2
s3
'''

# The factory to create solvers
class SolverFactory:
	def __init__(self, solver_path):
			self.s1_path = solver_path[0]
			self.s2_path = solver_path[1]
			self.s3_path = solver_path[2]

	def create_s1(self):
		return Solver('s1', self.s1_path)

	def create_s2(self):
		return Solver('s2', self.s2_path)

	def create_s3(self):
		return Solver('s3', self.s3_path)


	def create_all(self):
		return [self.create_s1(), self.create_s2(), self.create_s3()]



# To construct solvers
class Solver:

	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.results = []
		self.times = []
		self.solved = 0

