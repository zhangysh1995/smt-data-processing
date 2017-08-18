import os
import pwd
import argparse
import configparser
import smt_tests as st
from smt_solver import SolverFactory
# from tools.ssh import scp_csv

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


def configure(args):
	config_file = args.config
	config = configparser.ConfigParser()

	with open(config_file, 'r') as f:
		for line in f:
			print(line)
		f.close()

	config.read(config_file)

	# initialize from configuration
	s1_path = config.get('s1', 'path')
	s2_path = config.get('s2', 'path')
	s3_path = config.get('s3', 'path')

	solver_path = [s1_path, s2_path, s3_path]

	# run the program
	factory = SolverFactory(solver_path)
	split_project(config.get('general', 'cases'), factory, cpus=int(config.get('general', 'cpus')))


def run():
	parser = argparse.ArgumentParser(description='Run all your smt2 cases via all solvers.')
	parser.add_argument('--config', type=str, help='point to your configuration files (e.g config.)')
	args = parser.parse_args()
	configure(args)


run()
# scp_csv()

