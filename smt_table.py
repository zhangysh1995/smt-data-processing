import pandas as pd
import numpy as np
import smt_io as sio
from smt_io import file_prefix_abs
import os

solvers = ['z3', 'stp', 'boolector', 'ppbv']
dirs = ['../Out/sage', '../Out/KLEE', '../Out/PP-CASE']

# conut queries
def count_queries(path):
	if os.path.exists(path):
		for path, dir, file in os.walk(path):
			if len(dir) != 0:
				dir = [os.path.join(path, i) for i in dir]
				while len(dir) > 0:
					count_queries(dir.pop())
			else:
				file =[f for f in file if f.split('.')[1] == 'smt2']
				# write_table(dir_name(path) + ',' + str(len(file)) + '\n')
				write_table(dir_name(path) + ' ' + str(len(file)))
				solver_table(path + '/')
				# print(path)
	else:
		print('Directory Missing ' + path)


def write_table(line):
	with open('/home/zhangysh1995/work/results/Out/table.txt', 'a+') as f:
		try:
			f.write(line)
			f.close()
		except FileNotFoundError:
			print('Error when saving result!')
	return

def dir_name(path):
	dir = ''
	piece = path.split('/')
	if 'KLEE' in piece:
		dir = 'KLEE'
	elif 'PP-CASE' in piece:
		dir = 'PP-CASE'
	elif 'sage' in piece:
		dir = 'sage'

	name = path[path.index(dir):].replace('/', '-')
	return name


def results_file(path):
	return abs + file_prefix_abs(path) + sio.now + 'all-result.csv'


def times_file(path):
	return abs + file_prefix_abs(path) + sio.now + 'all-time.csv'


def solver_table(path):
	results = results_file(path)
	times = times_file(path)

	for solver in solvers:
		data = pd.read_csv(results)
		df = pd.DataFrame(data, columns=[solver])
		write_table(df[df == 'unsat' or df == 'sat'].count(axis=0))
		data = pd.read_csv(times)
		df = pd.DataFrame(data, columns=[solver])
		write_table(df[df <= 30.0].sum())
	write_table('\n')


def dir_table(path):
	count_queries(path)


def all_table():
	for dir in dirs:
		dir_table(dir)


# dir_name('/home/zhangysh1995/ctags/KLEE/test')
# count_queries('/home/zhangysh1995/PPBV')
abs = '/home/zhangysh1995/work/results/Out/'
dir_table('/home/zhangysh1995/PPBV/sage')