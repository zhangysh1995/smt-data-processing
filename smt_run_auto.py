import os
import pwd
import argparse
import configparser
import smt_tests as st
from smt_solver import SolverFactory
# from tools.ssh import scp_csv

'''
Called by smt_run_all.py
This module is used to run tests automatically on the server
NO NEED to change if solvers are stable

'''


def username():
	return pwd.getpwuid(os.geteuid()).pw_name


def split_project(entrance, factory, cpus):
	if os.path.exists(entrance):
		for path, dir, file in os.walk(entrance):
			if len(dir) != 0:
				dir = [os.path.join(path, i) for i in dir]
				while len(dir) > 0:
					split_project(dir.pop(), factory, cpus)
			else:
				print('\n\n===== Tests under folder ' + path + ' =====')
				file = [os.path.join(path, f) for f in file if f.split('.').pop() == 'smt2']
				st.test_solver_parallel(file, factory, cpus)
			return
	else:
		print('Directory Missing ' + entrance)


'''
If you need to change the solvers, first get familiar with config.ini file
then change this following method to fit your changes
'''


def configure(config_file):
		with open(config_file, 'r') as f:
			try:
				for line in f:
					print(line)
				f.close()
			except FileNotFoundError as e:
				print(e)

		config = configparser.ConfigParser()
		config.read(config_file)

		# initialize from configuration
		z3_path = config.get('z3', 'path')
		stp_path = config.get('stp', 'path')
		pp_path = config.get('ppbv', 'path')
		boolector_path = config.get('boolector', 'path')
		ppf_path = config.get('ppbvf', 'path')

		solver_path = [z3_path, stp_path, boolector_path, pp_path, ppf_path]


		# run the program
		factory = SolverFactory(solver_path)
		split_project(config.get('general', 'cases'), factory, cpus=int(config.get('general', 'cpus')))


def run(config):
	configure(config)

