# coding: utf-8

# !/usr/bin/python3
import argparse
import multiprocessing
import os
import sys
import time
from os import kill
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import PIPE, Popen

from smt_io import find_smt2, split_list, combine_data, output_results_separate, output_results, output_cases
from smt_solver import SolverFactory


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
	output_results(Solvers, os.path.split(flist[0])[0] + '/')
	# output_results_separate(Solvers, cpu)
	print('Finished!')


# return z3_time, z3_solved, bo_time, bo_solved, pp_time, pp_solved
def test_solvers(path, Solvers):
	flist = find_smt2(path)
	output_cases(flist)
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
	# combine_data(cpus)

# cases = '/root/PP_CASE/curl'

# # test_solvers(cases, factory.create_all())
# parser = argparse.ArgumentParser(description='Run single file of smt2 cases')
# parser.add_argument('--configure', type=str, help='point to your customized configurations')
# parser.add_argument('--case', type=str, help='specify smt2 cases directory')
# args = parser.parse_args()
#
# # if sys.argv == 1:
# # 	print('Use -h for')
# # 	exit(0)
#
# if args.case == '':
# 	flist = find_smt2(cases)
# 	test_solver_parallel(cases)
# else:
# 	flist = find_smt2(args.case)
# 	test_solver_parallel(flist)

# flist = find_smt2('/home/zhangysh1995/ctags')
# test_solver_parallel(flist)
