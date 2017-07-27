import csv
import fileinput
import glob
import os
import time

import pandas as pd

solver_list = ['z3', 'stp', 'boolector', 'ppbv']

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


def split_list(alist, wanted_parts=1):
	length = len(alist)
	return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
			for i in range(wanted_parts)]


now = time.strftime('%Y-%m-%d-')


def file(solver):
	return now + solver + '.csv'


def file_withCPU(solver, cpu):
	return now + solver + str(cpu) + '.csv'

# combine files of the same sovler
def combine_data(cpu=4):
	for solver in solver_list:
		outfile = file(solver)
		for i in range(cpu):
			with open('Out/' + outfile, 'a+') as f:
				input = fileinput.input(file_withCPU(solver, i))
				f.writelines(input)
				f.flush()
				f.close()
	csvs = find_csv(os.getcwd())
	for csv in csvs:
		os.remove(csv)


# Save results to file
def output_results_separate(solver, cpu):
	newfile = file_withCPU(solver.name, cpu)
	with open(newfile, 'a+', newline='') as csvfile:
		fieldnames = ['result', 'time']
		try:
			spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
			spamwriter.writeheader()
			for i in range(len(solver.results)):
				result = solver.results[i]
				interval = solver.times[i]
				if result == 'sat':
					sat = 1
				else:
					sat = 0
				spamwriter.writerow({'result': sat, 'time': interval})
			# spamwriter.writerow(str(interval))
			csvfile.close()
		except IOError as e:
			print('File I/O error: '.format(e))


# Save results to a huge file
def output_results(Solvers, cpu):
	newfile = '../Out/' + now + 'all.csv'
	data = {}
	for solver in Solvers:
		data.update({solver.name: solver.times})
	df = pd.DataFrame(data)
	with open(newfile, 'a+') as f:
		try:
			if cpu == 0:
				df.to_csv(f, index=False)
			else:
				df.to_csv(f, index=False, header=False)
			f.close()
		except IOError as e:
			print('I/O error when saving results: ').format(e)


# output report
def output_report(Solvers, cpu):
	# show results and save
	with open('results.txt', 'a+') as f:
		try:
			for solver in Solvers:
				print(solver.name + ': ' + str(sum(solver.times)) + ' ' + str(solver.solved))
				output_results_separate(solver, cpu)
				f.write(solver.name + ' ' + str(sum(solver.times)) + '\n')
			f.close()
		except IOError as e:
			print('I/O error when saving results: ').format(e)