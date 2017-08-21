import os
import pwd


'''
Use this module to customize your solvers and the wau to create solver instances.
Now factory design pattern is used but not flexible enough if you have changed number of solver.
Consider port Java Proxy here as a solution to this problem
'''

# solvers we have now
'''
z3
stp
ppbv
boolector
ppbvf
s0-s6
s0-s2
'''


# The factory to create solvers
class SolverFactory:
	# please be careful with this method parameters
	# TODO: so ugly with hard-coded indexes
	def __init__(self, solver_path):
		if len(solver_path) >= 4:
			self.solver_No = len(solver_path)
			self.z3_path = solver_path[0]
			self.stp_path = solver_path[1]
			self.boolector_path = solver_path[2]
			self.pp_path = solver_path[3]
			if len(solver_path) > 4:
				self.ppf_path = solver_path[4]
		else:
			self.pp_path = solver_path[0]
			self.ppf_path = solver_path[1]

	def create_z3(self):
		return Solver('z3', self.z3_path)

	def create_stp(self):
		return Solver('stp', self.stp_path)

	def create_boolector(self):
		return Solver('boolector', self.boolector_path)

	def create_ppbv(self):
		return Solver('ppbv', self.pp_path)

	def create_ppbvF(self):
		return Solver('ppbvf', self.ppf_path)

	def create_all(self):
		if self.solver_No == 4:
			return [self.create_z3(), self.create_stp(),
					self.create_boolector(), self.create_ppbv()]
		else:
			return [self.create_z3(), self.create_stp(),
					self.create_boolector(), self.create_ppbv(), self.create_ppbvF()]

	def create_two_ppbv(self):
		if self.solver_No == 2:
			return [self.create_ppbv(), self.create_ppbvF()]
		else:
			print('Error when creating different versions of ppbv!')
			exit(-1)


# To construct solvers
class Solver:
	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.results = []
		self.times = []
		self.solved = 0
