import pandas as pd
import numpy as np
import smt_io as sio
import os

solvers = ['boolector', 'z3', 'stp', 'ppbv', 'ppbvf']
dirs = ['sage', 'KLEE', 'PP-CASE']

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
				write_table(dir_name(path) + ' & ' + str(len(file)) + ' & ')
				solver_table(path + '/', len(file))
			return
	else:
		print('Directory Missing ' + path)


def write_table(line):
	with open('/home/zhangysh1995/work/results/Out/Table3.txt', 'a+') as f:
		try:
			f.write(str(line))
			f.close()
		except FileNotFoundError:
			print('Error when saving result!')
	return

def dir_name(path):
	# dir = ''
	# piece = path.split('/')
	# if 'KLEE' in piece:
	# 	dir = 'KLEE'
	# elif 'PP-CASE' in piece:
	# 	dir = 'PP-CASE'
	# elif 'sage' in piece:
	# 	dir = 'sage'
	#
	# name = path[path.index(dir)+len(dir):].replace('/', '-')
	return os.path.basename(path)


def results_file(path):
	return abs + sio.file_prefix_abs(path) + sio.now + 'all-result.csv'


def times_file(path):
	return abs + sio.file_prefix_abs(path) + sio.now + 'all-time.csv'


def solver_table(path, query_no):
	results = results_file(path)
	times = times_file(path)
	line = ''
	for solver in solvers:
		# print solved instance
		data = pd.read_csv(results)
		df = pd.DataFrame(data, columns=[solver])
		unsolved = query_no - int(df[df[solver].str.contains('sat')].count().to_string(index=False))
		line += str(unsolved) + ' & '
		# print total time
		data = pd.read_csv(times)
		df = pd.DataFrame(data, columns=[solver])
		line += df[df <= 30.0].sum().to_string(index=False, float_format='{:,.0f}'.format)
		line += ' && '
	write_table(line + '\\\\\n')


def dir_table(path):
	count_queries(path)


def all_table():
	# for dir in dirs:
	# 	dir_table('/home/zhangysh1995/PPBV/'+ dir)
	dir_table('/home/zhangysh1995/PPBV/KLEE')
		# write_table('\\hline\n')


# dir_name('/home/zhangysh1995/ctags/KLEE/test')
# count_queries('/home/zhangysh1995/PPBV')
abs = '/home/zhangysh1995/work/results/Out/'
# dir_table('/home/zhangysh1995/PPBV/sage')
all_table()