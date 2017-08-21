import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Usage:
import smt_analyze as sal
'''

# Example
# data = read_data('Out/xxx.csv')
# hist_t_query(data)
# plt.show() # Remember to add this line


'''
Below are function definitions
'''

# solvers = ['s1', 's2', 's3']
solvers = ['s0', 's1', 's2', 's3', 's4', 's5', 's6']
name = ['$TP_{none}$', '$TP_{light}$', '$TP_{heavy}$']
colors =['orange', 'dodgerblue', 'limegreen', 'pink', 'gray', 'purple', 'brown']
markers = ['d', 's', 'x', '+', 'o', '^', 'p']


def read_data(csv):
	data = pd.read_csv(csv)
	data.head()
	return data


# sum running time
def run_time(data):
	return pd.DataFrame(data.sum(axis=0))


# naive way to compare time
def com_time(data):
	df = pd.DataFrame(data.sum(axis=0))
	df.plot.bar(stacked=True)


def time_sovled(file):
	data = pd.read_csv(file)

	times = []
	for solver in solvers:
		time = data[solver]
		time = [t for t in time if t <= 15.0]
		times.append(time)

	rows = len(times[1])
	Xticks =[int(x) for x in np.linspace(0, rows, 51)]

	for i, time in enumerate(times):
		cumsum = []
		for tick in Xticks:
			cumsum.append(sum(time[:int(tick)]))
		plt.xlim(0, rows+500)
		plt.plot(Xticks, cumsum, label=solvers[i], color=colors[i], marker=markers[i], markersize=5)

	plt.xlabel('Solved instances')
	plt.ylabel('Cumulative running time/s')
	plt.legend()
	plt.savefig('pre-processing.png', bbox_inches='tight')


def table(tFile, rFile):
	times = pd.read_csv(tFile)
	results = pd.read_csv(rFile)

	for i, solver in enumerate(solvers):
		print(name[i], end=' ')
		time = times[solver].values
		result = results[solver].values
		i = 0
		for r in result:
			if 'sat' in r or 'unsat' in r:
				i += 1
		print('{:.0f} {}'.format(sum(time), 10000 - i))


time_sovled('../Out/2017-08-18-all-time.csv')
# table('../Out/2017-08-18-all-time.csv', '../Out/2017-08-18-all-result.csv')
plt.show()