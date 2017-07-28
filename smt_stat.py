import numpy as np
import matplotlib.pyplot as plt

from smt_io import file
solvers = ['z3', 'stp', 'boolector', 'ppbv']
colors = ['g', 'c', 'b', 'r', 'y']
markers = ['x', '^', 's', 'o', '+']


def single_data(solver):
	data = np.genfromtxt('../Out/' + file(solver), delimiter=',')
	return data

def	all_data():
	datas = []
	for solver in solvers:
		data = np.genfromtxt('../Out/' + file(solver), delimiter=',')
		datas.append(data)
	return datas


def all_time():
	times = []
	datas = all_data()
	for data in datas:
		times.append(data[:, 1])
	return times


def all_result():
	results = []
	datas = all_data()
	for data in datas:
		results.append(data[:, 0])
	return results

def count_query():
	data = single_data('z3')
	num = data.size
	print(num)

# pie chart on equal intervals
def time_distri_equal(solver):
	data = single_data(solver)
	times = data[:, 1]
	interval = np.linspace(0, 1, 6)
	y = np.zeros(len(interval))

	for time in times:
		for i in range(len(interval)):
			if i == 0:
				continue
			if interval[i] > time > interval[i-1]:
				y[i] += 1
	plt.pie(y/sum(y))


# pie cahart on non-equal intervals
def time_distri(solver):
	data = single_data(solver)
	time = data[:, 1]
	distri = np.histogram(time[1:], bins=(0.0, 0.02, 0.04, 0.06, 0.08))
	plt.pie(distri[1], labels=[0.0, 0.01, 0.02, 0.04, 0.06])
	plt.legend()


# distribution of time vs. solved instance
def	time_solved(instances, tick):
	ticks = np.linspace(0, instances, tick)
	times = all_time()

	index = 0
	for time in times:
		cumsum = []
		for tick in ticks:
			cumsum.append(sum(time[1:int(tick)]))
		plt.plot(ticks, cumsum, label=solvers[index], color=colors[index], marker=markers[index], markersize=5)
		index += 1

	plt.xlabel('solved')
	plt.ylabel('time')
	plt.title('Time to solve an instance')
	plt.legend()
