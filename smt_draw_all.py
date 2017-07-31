import matplotlib.pyplot as plt
from smt_stat import solvers
import smt_stat as stat
import smt_analyze as sal
from smt_draw import hist_t_query
import smt_io as sio
import pandas as pd
import numpy as np
import os.path
import glob
import math


def multi_time_query(csv):
	index = range(len(solvers))
	fig, axes = plt.subplots(nrows=4)
	data = sal.read_data(csv)
	for solver in solvers:
		bin = index[solvers.index(solver)]
		hist_t_query(data, solver, ax=axes[bin])

# def multi_time:
#
# multi_time_query('resultsample/dircolors-2017-07-28-all.csv')
# plt.show()


def all_time_query(path):
	csv = sio.find_csv_depth(path)
	for axis in axes:
		axis.set_xticks(range(len(csv)))
	for c in csv:
		multi_time_query(c)


# all_time_query('../Out')
# plt.show()


# combine time for one set
def draw_comb_time(path):
	draw_time(cat_data(path))


# cat data for one set together
def cat_data(path):
	csv = sio.find_csv(path)
	csv_all = [pd.read_csv(f) for f in csv]
	df = [pd.DataFrame(d) for d in csv_all]
	# print(df)
	data = pd.concat(df)
	return data

def draw_time(data):
	df = pd.DataFrame(data)
	# index = np.where(df['z3'].notnull())[0]
	# print(index)
	cumsum = []
	ticks = [i for i in np.linspace(0, 10000, 51)]
	for i in ticks:
		cumsum.append(df.iloc[:int(i)].sum())
	d = pd.DataFrame(cumsum)
	d.plot()
	# d.plot()

def comp_time(path):
	csv = glob.glob(path + '/*.csv')
	rows = math.ceil(math.sqrt(len(csv)))
	fig, axis = plt.subplots(nrows=int(rows), ncols=int(rows))

	for c in csv:
		df = pd.DataFrame(pd.read_csv(c))
		index = csv.index(c)
		for solver in stat.solvers:
			print(index, solver, c)
			df.plot.scatter(x=solver, y='ppbv', ax=axis[int(index/rows) -1, int(index%rows)])
			prefix = os.path.basename(c).split('.')[0]
			plt.savefig('../plots/klee-' + solver + '-' + str(prefix))

# draw_time('resultsample/dircolors-2017-07-28-all.csv')
draw_comb_time('../Out/sage')
# cat_data('../Out/sage')
plt.show()