import os
import pwd
import argparse
import configparser
import smt_tests as st
from smt_solver import SolverFactory
# from tools.ssh import scp_csv

'''
Similar to smt_run_auto, but this module it for running the benchmarks manually
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


def configure(args):
	config_file = args.config
	config = configparser.ConfigParser()

	if args.config is None:
		print('====== Use -h for help if you want configuration file ======')
		if username() == 'zhangysh1995':  # configure on my local desktop
			z3_path = '/home/zhangysh1995/work/ppdev/z3/build/z3'
			stp_path = '/home/zhangysh1995/work/stp/stp/build/stp-2.1.2 --SMTLIB2'
			boolector_path = '/home/zhangysh1995/work/boolector-2.4.1/boolector/bin/boolector --smt2'
			pp_path = '/home/zhangysh1995/work/ppdev/ppsat/ppbv'
			ppf_path = ''
		else:  # configure on sbtest1 docker image
			z3_path = '/root/Solvers/z3-4.5.0/build/z3'
			stp_path = '/root/Solvers/stp/stp/build/stp-2.1.2'
			boolector_path = '/root/Solvers/boolector-2.4.1/boolector/bin/boolector --smt2'
			pp_path = '/root/Solvers/ppsat/build-dev/ppbv --array'
			ppf_path = '/root/Sovlers/ppsat-layer/build-dev/ppbv --array --layer'
		solver_path = [z3_path, stp_path, boolector_path, pp_path, ppf_path]
		factory = SolverFactory(solver_path)
		cases = input('Path to your cases: ')
		cpus = input('CPU cores: ')
		split_project(cases, factory, cpus=int(cpus))
	else:
		with open(config_file, 'r') as f:
			for line in f:
				print(line)
			f.close()

		read = input('Continue?(y/n) ')
		if read == 'n':
			exit(0)
		config.read(config_file)

		choice = input('Run which solvers? a.3+1, b.3+2, c.2')

		# initialize from configuration
		z3_path = config.get('z3', 'path')
		stp_path = config.get('stp', 'path')
		pp_path = config.get('ppbv', 'path')
		boolector_path = config.get('boolector', 'path')
		ppf_path = config.get('ppbvf', 'path')

		# customize solvers
		if choice == 'c':
			solver_path = [pp_path, ppf_path]
		elif choice == 'b':
			solver_path = [z3_path, stp_path, boolector_path, pp_path, ppf_path]
		else:
			solver_path = [z3_path, stp_path, boolector_path, pp_path]

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
