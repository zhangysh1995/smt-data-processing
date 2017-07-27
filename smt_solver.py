import os

'''
z3
stp
ppbv
boolector
'''

if os.getlogin() == 'zhangysh1995':  # configure on my local desktop
	z3_path = '/home/zhangysh1995/work/ppdev/z3/build/z3'
	stp_path = '/home/zhangysh1995/work/stp/stp/build/stp-2.1.2 --SMTLIB2'
	pp_path = '/home/zhangysh1995/work/ppdev/ppsat/ppbv'
	boolector_path = '/home/zhangysh1995/work/boolector-2.4.1/boolector/bin/boolector --smt2'
elif os.getlogin() == 'root':  # configure on sbtest1 docker image
	z3_path = '/root/Solvers/z3-4.5.0/build/z3'
	stp_path = '/root/Solvers/stp/stp/build/stp-2.1.2'
	pp_path = '/root/Solvers/ppsat/build-dev/ppbv'
	boolector_path = '/root/Solvers/boolector-2.4.1/boolector/bin/boolector --smt2'
else:
	print('Wrong user!')
	exit(-1)


# The factory to create solvers
class SolverFactory:
	@staticmethod
	def create_z3():
		return Solver('z3', z3_path)

	@staticmethod
	def create_stp():
		return Solver('stp', stp_path)

	@staticmethod
	def create_boolector():
		return Solver('boolector', boolector_path)

	@staticmethod
	def create_ppbv():
		return Solver('ppbv', pp_path)

	def create_all(self):
		return [self.create_z3(), self.create_stp(),
				self.create_boolector(), self.create_ppbv()]

# To construct solvers
class Solver:
	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.results = []
		self.times = []
		self.solved = 0