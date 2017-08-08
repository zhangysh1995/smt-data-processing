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
				file = [os.path.join(path, f) for f in file if f.split('.')[1] == 'smt2']
				st.test_solver_parallel(file, factory, cpus)
			return
	else:
		print('Directory Missing ' + entrance)

parser = argparse.ArgumentParser(description='Run all your smt2 cases via all solvers.')
parser.add_argument('--config', type=str, help='point to your configuration files (e.g config.)')
parser.add_argument('--case', type=str, help='absolute path to your test cases root directory')
parser.add_argument('--cpus', type=int, help='how many cpus cores you want to use? (Better under 24)')
args = parser.parse_args()


cpus = 0
solver_path = []

if args.config is None:
	if username() == 'zhangysh1995':  # configure on my local desktop
		z3_path = '/home/zhangysh1995/work/ppdev/z3/build/z3'
		stp_path = '/home/zhangysh1995/work/stp/stp/build/stp-2.1.2 --SMTLIB2'
		pp_path = '/home/zhangysh1995/work/ppdev/ppsat/ppbv'
		boolector_path = '/home/zhangysh1995/work/boolector-2.4.1/boolector/bin/boolector --smt2'
	else:   # configure on sbtest1 docker image
		z3_path = '/root/Solvers/z3-4.5.0/build/z3'
		stp_path = '/root/Solvers/stp/stp/build/stp-2.1.2'
		pp_path = '/root/Solvers/ppsat-array/build-dev/ppbv'
		boolector_path = '/root/Solvers/boolector-2.4.1/boolector/bin/boolector --smt2'
	solver_path = [z3_path, stp_path, pp_path, boolector_path]
else:
	config_file = args.config
	config = configparser.ConfigParser()
	config.read(config_file)
	z3_path = config.get('z3', 'path')
	stp_path = config.get('stp', 'path')
	pp_path = config.get('ppbv', 'path')
	boolector_path = config.get('boolector', 'path')
	solver_path = [z3_path, stp_path, pp_path, boolector_path]
	print(solver_path)

if args.cpus is None:
	pass
else:
	cpus = args.cpus

factory = SolverFactory(solver_path)

if args.case is None:
	if username() == 'zhangysh1995':
		split_project('/home/zhangysh1995/ctags', factory, cpus)
	else:
		split_project('/root/PPBV', factory, cpus)
else:
		split_project(args.case, factory, cpus)

# scp_csv()