import csv
import fileinput
import glob
import os
import time

import pandas as pd

solver_list = ['z3', 'stp', 'boolector', 'ppbv', 'ppbvf']


# find cnf files in path
def find_cnf(path):
	flist = []  # path to DIMACS files
	for root, dirs, files in os.walk(path):
		for fname in files:
			# confirm the file format
			if os.path.splitext(fname)[1] == '.cnf':
				flist.append(os.path.join(root, fname))
	return flist


# find smt2 files in path
def find_smt2(path):
	flist = []  # path to smtlib2 files
	if path != None and os.path.exists(path):
		for root, dirs, files in os.walk(path):  # search the directory
			for fname in files:
				if os.path.splitext(fname)[1] == '.smt2':
					flist.append(os.path.join(root, fname))
		return flist
	else:
		print('Use -h for help')
		exit(-1)


def find_csv(path):
	return glob.glob(path + '/*.csv')


def find_csv_depth(path):
	flist = []  # path to DIMACS files
	for root, dirs, files in os.walk(path):
		for fname in files:
			# confirm the file format
			if os.path.splitext(fname)[1] == '.csv':
				flist.append(os.path.join(root, fname))
	return flist


# cat data for one set together
def cat_data(path, solver=None):
	csv = find_csv(path)
	if solver is None:
		data = pd.concat((pd.read_csv(f) for f in csv), ignore_index=True)
		return data
	else:
		data = pd.concat((pd.read_csv(f, usecols=[solver]) for f in csv), ignore_index=True)
		return data


# cat data to be a dict, which is better to use with Pandas
def cat_data_dict(csv, solver):
	data = {}
	for c in csv:
		df = pd.DataFrame(pd.read_csv(c), columns=[solver])
		data.update({get_name(c): df.to_dict()[solver]})
	return pd.DataFrame.from_dict(data, orient='columns')


# extracted from smt_tests
# used to split the file list into parts for multi-core processing
def split_list(alist, wanted_parts=1):
	length = len(alist)
	return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
			for i in range(wanted_parts)]


# find corresponding dir and filename for cases
# **ugly implementation**
def file_prefix(path):
	dir = ''
	piece = path.split('/')
	if 'KLEE' in piece:
		dir = 'KLEE'
	elif 'PP-CASE' in piece:
		dir = 'PP-CASE'
	elif 'sage' in piece:
		dir = 'sage'

	return dir, path[path.index(dir)+len(dir)+1:].replace('/', '-')


def file_prefix_rela(path):
	prefix = file_prefix(path)
	return '../Out/' + os.path.join(prefix[0], prefix[1])


def file_prefix_abs(path):
	prefix = file_prefix(path)
	print(file)
	return os.path.join(prefix[0], prefix[1])


# filename formatter for output csvs
now = time.strftime('%Y-%m-%d-')


def file(solver):
	return now + solver + '.csv'


def file_withCPU(solver, cpu):
	return now + solver + str(cpu) + '.csv'


# get project from filename
def get_name(path):
	file = os.path.split(path)[1]
	return file[:file.find('-2017')]


# combine files of the same sovler
def combine_data(cpu=4, path=''):
	for solver in solver_list:
		outfile = file_prefix_rela(path) + file(solver)
		for i in range(cpu):
			with open(outfile, 'a+') as f:
				try:
					input = fileinput.input(file_withCPU(solver, i))
					f.writelines(input)
					f.flush()
					f.close()
				except IOError as e:
					print('File I/O error: '.format(e))
	csvs = find_csv(os.getcwd())
	for csv in csvs:
		os.remove(csv)


# Save results to file
def output_results_separate(Solvers, cpu):
	for solver in Solvers:
		newfile = file_withCPU(solver.name, cpu)
		with open(newfile, 'a+', newline='') as csvfile:
			fieldnames = ['result', 'time']
			try:
				spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
				if cpu == 0:
					spamwriter.writeheader()

				for i in range(len(solver.results)):
					result = solver.results[i]
					interval = solver.times[i]
					if result == 'sat':
						sat = 1
					else:
						sat = 0
					spamwriter.writerow({'result': sat, 'time': interval})
				csvfile.close()
			except IOError as e:
				print('File I/O error: '.format(e))

# Save results to a huge file
def output_results(Solvers, path, flist=None):
	newfile1 = file_prefix_rela(path) + now + 'all-time.csv'
	newfile2 = file_prefix_rela(path) + now + 'all-result.csv'
	flist = [os.path.basename(f) for f in flist]
	# TODO: multicore variable competition here for `header`
	if(os.path.isfile(newfile1)):
		header = False
	else:
		header = True

	# save time
	data = {}
	data.update({'case': flist})
	for solver in Solvers:
		data.update({solver.name: solver.times})
	df = pd.DataFrame(data)
	with open(newfile1, 'a+') as f:
		try:
			df.to_csv(f, index=False, header=header)
			f.close()
		except IOError as e:
			print('I/O error when saving results: ')
	data.clear()

	# save results
	data.update({'case': flist})
	for solver in Solvers:
		data.update({solver.name: solver.results})
	df = pd.DataFrame(data)
	with open(newfile2, 'a+') as f:
		try:
			df.to_csv(f, index=False, header=header)
			f.close()
		except IOError as e:
			print('I/O error when saving results: ')


# output the smt2 filenames to a file
def output_cases(flist):
	# output case names
	with open('CaseNames.txt', 'w') as CaseNames:
		for item in flist:
			CaseNames.write('%s\n' % os.path.split(item)[1])
