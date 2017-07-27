# coding: utf-8

# !/usr/bin/python3
import time
import os
import csv
import pandas as pd
import multiprocessing
import glob
import fileinput
import argparse

from os import kill
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import PIPE, Popen

# usage: python3 smt_tests.py config.json

# fill the path to fit your files' location

solver_list = ['z3', 'stp', 'boolector', 'ppbv']
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
	stp_path = '/root/Solvers/stp/stp/build/stp-2.1.2 --SMTLIB2'
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

def split_list(alist, wanted_parts=1):
	length = len(alist)
	return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
			for i in range(wanted_parts)]


def find_csv(path):
	return glob.glob(path + '/*.csv')

# file naming format
now = time.strftime('%Y-%m-%d-')


# filename of csv
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
	newfile = 'Out/' + now + 'all.csv'
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


class TestResult:
	def __init__(self, runtime, result, verify, error):
		self.runtime = runtime
		self.result = result
		self.verify = verify
		self.error = error

	def __str__(self):
		return self.runtime + '\t' + self.result + '\t' + self.verify + '\t' + self.error


class TestCase:
	def __init__(self, filename):
		self.filename = filename
		self.solverResult = {}


# get children to run in parallel mode
def get_process_children(pid):
	p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	return [int(p) for p in stdout.split()]


# Run a command with a timeout, after which it will be forcibly killed.
def run(args, cwd=None, shell=False, kill_tree=True, timeout=1, env=None):
	'''
	Run a command with a timeout after which it will be forcibly
	killed.
	'''

	class Alarm(Exception):
		pass

	def alarm_handler(signum, frame):
		raise Alarm

	p = Popen(args, shell=shell, cwd=cwd, stdout=PIPE, stderr=PIPE, env=env)
	if timeout != -1:
		signal(SIGALRM, alarm_handler)
		alarm(timeout)
	try:
		stdout, stderr = p.communicate()
		stdout = stdout.decode(encoding='ascii')
		stderr = stderr.decode(encoding='ascii')
		if timeout != -1:
			alarm(0)
	except Alarm:
		pids = [p.pid]
		if kill_tree:
			pids.extend(get_process_children(p.pid))
		for pid in pids:
			# process might have died before getting to this line
			# so wrap to avoid OSError: no such process
			try:
				kill(pid, SIGKILL)
			except OSError:
				pass
		return -9, '', ''
	return p.returncode, stdout, stderr


# TODO. make `unknown` and `timeout` different
def test_with_solver(solver, testfile, timeout):
	runtime = ''
	result = ''
	verify = ''
	error = ''

	try:
		startTime = time.time()
		(exitCode, output, errors) = run(solver.path + ' ' + testfile, shell=True, timeout=timeout)
		endTime = time.time()
		runtime = endTime - startTime
		if len(output) == 0:
			result = 'timeout'
		else:
			lines = output.split('\n')
			errlines = errors.split('\n')

			combined_lines = ''
			for line in lines:
				combined_lines += ' ' + line
			for line in errlines:
				combined_lines += ' ' + line

			lines = [line for line in lines if line.strip()]
			# check result status
			# !!!! This must be simplified
			for line in lines:
				if 'unsat' in line:
					result = 'unsat'
					error = ''
					solver.solved += 1
					break
				elif 'sat' in line:
					result = 'sat'
					error = ''
					solver.solved += 1
					break
				elif 'unknown' in line:
					result = 'unknown'
					error = ''
					break
				else:
					result = 'error'
					error = combined_lines
	# TODO verify, and check verify status
	except Exception as e:
		print(e)
		result = 'crash'
		error = str(e)

	return TestResult(runtime, result, verify, error)


def compare_solvers(flist, Solvers, cpu=0):
	# run cases with all solvers
	for fname in flist:
		print('Testing... ' + os.path.split(fname)[1])
		for solver in Solvers:
			# print(solver.name + ' ', flush = False)
			testResult = test_with_solver(solver, fname, 2)
			solver.results.append(testResult.result)
			solver.times.append(testResult.runtime)
	output_report(Solvers, cpu)
	output_results(Solvers, cpu)
	print('Finished!')


# return z3_time, z3_solved, bo_time, bo_solved, pp_time, pp_solved
def test_solvers(path, Solvers):
	flist = find_smt2(path)
	# output case names
	with open('CaseNames.txt', 'w') as CaseNames:
		for item in flist:
			CaseNames.write('%s\n' % os.path.split(item)[1])
	# run the tests
	compare_solvers(flist, Solvers)


factory = SolverFactory()

def test_solver_parallel(flist):
	print('-------------Started!------------')
	print('Total files', len(flist))
	print('')
	multiprocessing.freeze_support()
	pool = multiprocessing.Pool()
	cpus = multiprocessing.cpu_count()
	files = split_list(flist, cpus)
	for i in range(0, cpus):
		pool.apply_async(compare_solvers, args=(files[i], factory.create_all(), i))
	pool.close()
	pool.join()
	print('All Finished!')
	combine_data(cpus)


# test_solvers(cases, factory.create_all())
parser = argparse.ArgumentParser(description='SMT solver testing config')
parser.add_argument('--configure', type=str, help='point to your customized configurations')
parser.add_argument('--case', type=str, help='specify smt2 cases directory')
# args = parser.parse_args()
# if sys.argv == 1:
# 	print('Use -h for')
# if args.case == '':
# 	test_solver_parallel(cases)
# else:
# 	test_solver_parallel(args.case)
# flist = find_smt2(args.case)
# test_solver_parallel(flist)
