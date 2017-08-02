import matplotlib.pyplot as plt
import matplotlib.style
# matplotlib.style.use('seaborn-paper')
from matplotlib import gridspec
import matplotlib.ticker as mtick
import smt_io as sio
import pandas as pd
import numpy as np
import os.path
import glob
import math

dirs = ['../Out/sage', '../Out/KLEE', '../Out/PP-CASE']
solvers = ['z3', 'stp', 'boolector', 'ppbv']

xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 15.0, 30.0]
ticks = [0.1, 1.0, 2.0, 15, 35]
colors = ['g', 'c', 'b', 'r', 'y']
markers = ['x', '^', 's', 'o', '+']
width=0.2

x = np.arange(0, 30, 5)
equal = pd.DataFrame({'x': x, 'y': x})
double = pd.DataFrame({'x': x, 'y': x * 2})
half = pd.DataFrame({'x': x, 'y': x * 1/2})


# get project from filename
def get_name(path):
	file = os.path.split(path)[1]
	return file[:file.find('-2017')]


# draw reference liens
def draw_refe(ax):
	equal.plot(x='x', y='y', legend=False, style='r--', ax=ax)
	double.plot(x='x', y= 'y', legend=False, style='g--', ax=ax)
	half.plot(x='x', y = 'y', legend=False, style='g--', ax=ax)


# combine time for one set
# TODO: markers and axis
def comb_time_all():
	for dir in dirs:
		draw_time(sio.cat_data(dir), dir)

#
def time_sovled(data):
	df = pd.DataFrame(data)
	rows, columns = df.shape
	X = np.linspace(0, rows, 51)
	X = [int(x) for x in X]
	cumsum = []
	for i in X:
		cumsum.append(df.loc[:i].sum())

	d = pd.DataFrame(cumsum)
	for solver in solvers:
		index = solvers.index(solver)
		ax = d[solver].plot(color=colors[index], marker=markers[index], markersize=3)
		ax.set_xticklabels(X*10)


def hist_t_query(df, ax):
	count = []
	all = df.count(axis=0)
	time = []
	sum = df.sum(axis=0)
	rot = 45
	for i in range(len(ticks)):
		count.append((df[df < ticks[i]].count()) / all * 100)
		time.append((df[df < ticks[i]].sum()) / sum * 100)
		color = colors[i]

		if i == 0:
			count[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=-0.05)
			time[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=1.05)
		else:
			(count[i] - count[i - 1]).plot(kind='bar', bottom=count[i - 1],
										   ax=ax, rot=rot, color=color, width=width, position=-0.05)
			(time[i] - time[i - 1]).plot(kind='bar', bottom=time[i - 1],
										 ax=ax, rot=rot, color=color, width=width, position=1.05)


# cumsum time
def draw_time(data, dir = ''):
	fig, axis = plt.subplots()
	df = pd.DataFrame(data)
	cumsum = []
	ticks = [i for i in np.linspace(0, 10000, 51)]
	for i in ticks:
		cumsum.append(df.iloc[:int(i)].sum())
	# d = pd.DataFrame(cumsum)
	# ax = d.plot(xticks=ticks)
	# fig = ax.get_figure()
	# fig.savefig('../plots/' + dir.split('/').pop() + '.png')
	plt.plot(ticks, cumsum)
	plt.savefig(dir.split('/').pop() + '.png')



# draw separately
def comp_time(path):
	project = path.split('/').pop()
	csv = glob.glob(path + '/*.csv')
	fig, ax = plt.subplots()

	for c in csv:
		for solver in solvers:
			if solver == 'ppbv':
				continue
			df = pd.DataFrame(pd.read_csv(c))
			index = csv.index(c)
			print(index, solver, c)
			ax.set_xlim([0, 30])
			ax.set_ylim([0, 30])
			ax.set_xticks([0, 1, 5, 15, 30])
			df.plot(kind='scatter', x=solver, y='ppbv',  ax=ax, legend=False,
					color='k', marker='x')
			draw_refe(ax)
			plt.savefig('../plots/'+ project + '/' + solver + '-' + os.path.split(c)[1] + '.png')


def comp_time_project(path):
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
		plt.close()


def time_query_project(path):
	csv = sio.find_csv(path)
	# create shared x-axis
	gs = gridspec.GridSpec(4, 1)
	ax0 = plt.subplot(gs[0])

	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)

	data = {}
	for solver in solvers:
		for c in csv:
			df = pd.DataFrame(pd.read_csv(c), columns=[solver])
			data.update({get_name(c): df.to_dict()[solver]})
		df = pd.DataFrame.from_dict(data, orient='columns')
		ax = plt.subplot(gs[solvers.index(solver)], sharex=ax0)
		ax.yaxis.set_major_formatter(yticks)
		ax.set_ylabel(solver)
		hist_t_query(df, ax)

'''
wrappers for functions beyond
'''


# draw for all projects
def comp_time_all():
	for dir in dirs:
		comp_time_matrix(dir)


# draw for single projects
def comp_time_single():
	for dir in dirs:
		comp_time_project(dir)


# draw single plots
def comp_time_all_single():
	for dir in dirs:
		comp_time(dir)


# draw cumsum vs. time
def time_solved_all():
	for dir in dirs:
		folder = dir.split('/').pop()
		# plt.title(folder)
		plt.xlabel('Solved instances')
		plt.ylabel('Cumulative running time/s')
		time_sovled(sio.cat_data(dir))
		plt.legend()
		plt.savefig('../plots/' + folder + '-time-solved.png')
		plt.close()
		print('figure')

# draw time_query
def time_query():
	for dir in dirs:
		folder = dir.split('/').pop()
		time_query_project(dir)
		plt.savefig('../plots/' + folder + '-time-query')
# draw time&query vs. solved
# def time_query_all():


'''
Below are usages
'''

# comb_time_all()

# comp_time_all()
# comp_time_single()
# comp_time_all_single()
# comp_time('../Out/KLEE')

# time_query_project('../Out/KLEE')
# time_query()

time_solved_all()
# time_sovled(pd.read_csv('resultsample/dircolors.csv'))
# time_sovled(sio.cat_data('../Out/KLEE'))

# plt.show()



