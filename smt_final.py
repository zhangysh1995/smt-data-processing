import os
import argparse
import smt_tests as st


def split_project(entrance):
	if os.path.exists(entrance):
		for path, dir, file in os.walk(entrance):
			if len(dir) != 0:
				dir = [os.path.join(path, i) for i in dir]
				while len(dir) > 0:
					split_project(dir.pop())
			else:
				print('\n\n===== Tests under folder ' + path + ' =====')
				st.test_solver_parallel(file)
			return
	else:
		print('Directory Missing ' + entrance)

parser = argparse.ArgumentParser(description='Run all your smt2 cases via all solvers.')
parser.add_argument('--case', type=str, help='absolute path to your test cases root directory')
args = parser.parse_args()

if args.case == None:
	if os.getlogin() == 'zhangysh1995':
		split_project('/home/zhangysh1995/ctags')
	elif os.getlogin() == 'root':
		split_project('/root/PPBV')
else:
	split_project(args.case)