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

dirs = ['../Out/sage', '../Out/KLEE', '../Out/PP-CASE']

fig, axes = plt.subplots(nrows=4)

def multi_time_query(csv):
	index = range(len(solvers))
	data = sal.read_data(csv)
	for solver in solvers:
		bin = index[solvers.index(solver)]
		hist_t_query(data, solver, ax=axes[bin])


def all_time_query(path):
	csv = sio.find_csv_depth(path)
	for axis in axes:
		axis.set_xticks(range(len(csv)))
	for c in csv:
		multi_time_query(c)


# all_time_query('../Out')
# plt.show()


# combine time for one set
# TODO: markers and axis
def draw_comb_time(path):
	draw_time(cat_data(path))


# cumsum time
def draw_time(data):
	df = pd.DataFrame(data)
	cumsum = []
	ticks = [i for i in np.linspace(0, 10000, 51)]
	for i in ticks:
		cumsum.append(df.iloc[:int(i)].sum())
	d = pd.DataFrame(cumsum)
	d.plot()
	# d.plot()


# cat data for one set together
def cat_data(path):
	csv = sio.find_csv(path)
	csv_all = [pd.read_csv(f) for f in csv]
	df = [pd.DataFrame(d) for d in csv_all]
	data = pd.concat(df)
	return data


def comp_time(path):
	project = path.split('/').pop()
	csv = glob.glob(path + '/*.csv')
	fig, axis = plt.subplots(ncols=3)

	for c in csv:
		for solver in solvers:
			if solver == 'ppbv':
				continue
			df = pd.DataFrame(pd.read_csv(c))
			index = csv.index(c)
			print(index, solver, c)
			ax = axis[solvers.index(solver)]
			ax.set_xticks([0, 0.1, 0.3, 0.5, 1.0, 2.0])
			df.plot.scatter(x=solver, y='ppbv', ax=ax)
		plt.savefig('../plots/'+ project + '/' + os.path.split(c)[1] + '.png')


# draw scatter for solvers vs. ppbv & save
def comp_time_matrix(path):
	project = path.split('/').pop()
	csv = glob.glob(path + '/*.csv')
	rows = math.ceil(math.sqrt(len(csv)))
	fig, axis = plt.subplots(nrows=int(rows), ncols=int(rows))

	out = pd.DataFrame(csv)
	x = np.arange(0, 2.0, 0.5)
	dc = pd.DataFrame({'x': x, 'y': x})

	for solver in solvers:
		if solver == 'ppbv':
			continue
		for c in csv:
			df = pd.DataFrame(pd.read_csv(c))
			index = csv.index(c)
			print(index, solver, c)
			ax = axis[int(math.floor(index/rows)), int(index%rows)]
			# ax.set_title(os.path.split(c)[1])
			ax.set_xticks([0, 0.1, 0.3, 0.5, 1.0, 2.0])
			df.plot.scatter(x=solver, y='ppbv', ax=ax)
			# dc.plot(x='x', y='y', ax=ax, legend=False, style='rx:')
		plt.savefig('../plots/'+ project + '-original-' + solver)

# draw for all projects
def comp_time_all():
	for dir in dirs:
		comp_time_matrix(dir)

# draw for single projects
def comp_time_single():
	for dir in dirs:
		comp_time(dir)

# draw_comb_time('../Out/KLEE')
# plt.show()

# comp_time_all()
# comp_time_single()