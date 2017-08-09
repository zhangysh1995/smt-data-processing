import os
import pwd

'''
z3
stp
ppbv
boolector
'''

# The factory to create solvers
class SolverFactory:
	def __init__(self, solver_path):
			self.solver_No = len(solver_path)
			self.z3_path = solver_path[0]
			self.stp_path = solver_path[1]
			self.boolector_path = solver_path[2]
			self.pp_path = solver_path[3]
			# if len(solver_path) > 4:
			# 	self.ppf_path = solver_path[4]

	def create_z3(self):
		return Solver('z3', self.z3_path)

	def create_stp(self):
		return Solver('stp', self.stp_path)

	def create_boolector(self):
		return Solver('boolector', self.boolector_path)

	def create_ppbv(self):
		return Solver('ppbv', self.pp_path)

	# def create_ppbvF(self):
	# 	return Solver('ppbvf', self.ppf_path)

	def create_all(self):
		if self.solver_No == 4:
			return [self.create_z3(), self.create_stp(),
					self.create_boolector(), self.create_ppbv()]
		# else:
			# do other things

# To construct solvers
class Solver:

	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.results = []
		self.times = []
		self.solved = 0
