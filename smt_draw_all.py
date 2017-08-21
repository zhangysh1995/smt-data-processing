import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.style

from smt_io import cat_data_dict

matplotlib.style.use('seaborn-paper')
from matplotlib import gridspec
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import smt_io as sio
import pandas as pd
import numpy as np
import os.path
import glob
import math

'''
All methods to draw the result plots
Wrappers of easy methods are at last
'''

dirs = ['../Out/sage', '../Out/KLEE', '../Out/PP-CASE']
cases = ['../PPBV/sage', '../PPBV/KLEE', '../PPBV/PP-CASE']
solvers = ['z3', 'stp', 'boolector', 'ppbv', 'ppbvf']

xticks = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 15.0, 30.0]
ticks = [0.1, 1.0, 2.0, 15.0, 30.0, math.inf]
colors = ['g', 'c', 'b', 'r', 'y', 'k']
markers = ['d', '^', 's', 'o', 'x']
width=0.2

x = np.arange(0, 30, 5)
equal = pd.DataFrame({'x': x, 'y': x})
double = pd.DataFrame({'x': x, 'y': x * 2})
half = pd.DataFrame({'x': x, 'y': x * 1/2})


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
	# rows, columns = data.shape
	# X = np.linspace(0, rows, 51)
	# X = [int(x) for x in X]
	# cumsum = []
	# for i in X:
	# 	cumsum.append(data.loc[:i].sum())
	# d = pd.DataFrame(cumsum)
	# for solver in solvers:
	# 	index = solvers.index(solver)
	# 	ax = d[solver].plot(color=colors[index], marker=markers[index], markersize=3)
	# 	ax.set_xticklabels(X*10)

	# write all data to tmp file
	with open('all.csv', 'w+') as f:
		csv = pd.DataFrame(data).to_csv(header=True, index=False)
		f.write(csv)
		f.close()

	times = []
	# datas = np.genfromtxt('all.csv', skip_header=1, delimiter=',')
	# datas = pd.read_csv('all.csv')

	for solver in solvers:
		time = data[solver]
		time = [t for t in time if float(t) <= 30.0]

		times.append(time)

	rows = len(times[1])
	Xticks =[int(x) for x in np.linspace(0, rows, 51)]

	for i, time in enumerate(times):
		cumsum = []
		for tick in Xticks:
			cumsum.append(sum(time[:int(tick)]))
		plt.xlim(0, rows+500)
		# plt.ylim(0, sum(time)))
		plt.plot(Xticks, cumsum, label=solvers[i], color=colors[i], marker=markers[i], markersize=5)

	plt.legend()

	# clean working directory
	# file = glob.glob('*.csv')
	# os.remove(file)

def hist_t_query(df, ax):
	count = []
	all = df.count(axis=0)
	time = []
	sum = df.sum(axis=0)
	rot = 45
	for i in range(len(ticks)):
		# query time
		nc = df[df < ticks[i]].count()
		nc = nc.fillna(0)
		count.append(nc / all * 100)

		# cumulitive time of the query solving time
		nt = df[df < ticks[i]].sum()
		nt = nt.fillna(value=0.0)
		time.append(nt / sum * 100)

		color = colors[i]

		if i == 0:
			count[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=1.05)
			time[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=-0.05)
		else:
			(count[i] - count[i - 1]).plot(kind='bar', bottom=count[i - 1],
										   ax=ax, rot=rot, color=color, width=width, position=1.05)
			(time[i] - time[i - 1]).plot(kind='bar', bottom=time[i - 1],
										 ax=ax, rot=rot, color=color, width=width, position=-0.05)
	return ax


# cumsum time
def draw_time(data, dir = ''):
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
	csv = glob.glob(path + '/*-time.csv')
	fig, ax = plt.subplots()

	for c in csv:
		for solver in solvers:
			if solver == 'ppbv':
				continue
			df = pd.DataFrame(pd.read_csv(c))
			index = csv.index(c)
			print(index, solver, c)

			# draw original plot
			ax.set_xlim([0, 30])
			ax.set_ylim([0, 30])
			ax.set_xticks([0, 1, 5, 15, 30])
			df.plot(kind='scatter', x=solver, y='ppbv',  ax=ax, legend=False,
					color='b', marker='x')

			# reference lines
			# draw_refe(ax)

			# draw zoom-in plot
			axins = zoomed_inset_axes(ax, 9, loc=1)
			axins.set_xlim(0, 1)
			axins.set_ylim(0, 1)
			plt.xticks(visible=False)
			plt.yticks(visible=False)
			axins.xaxis.set_visible(False)
			axins.yaxis.set_visible(False)
			mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec='gray')

			df.plot.scatter(x=solver, y='ppbv', ax=axins, subplots=True, legend=False,
					color='b', marker='x')

			plt.savefig('../plots/'+ project + '/' + solver + '-' + os.path.split(c)[1] + '.png')


def comp_time_project(path):
	project = path.split('/').pop()
	csv = glob.glob(path + '/*-time.csv')
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
	csv = glob.glob(path + '/*-time.csv')
	rows = math.ceil(math.sqrt(len(csv)))
	fig, axis = plt.subplots(nrows=int(rows), ncols=int(rows))

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
		plt.savefig('../plots/'+ project + '-original-' + solver)


def time_query_project(path):
	csv = sio.find_csv(path)
	plt.figure(figsize=(6, 4))
	# create shared x-axis
	gs = gridspec.GridSpec(4, 1)
	gs.update(hspace=0)
	ax0 = plt.subplot(gs[0])

	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)

	axis = []
	for solver in solvers[:-1]:
		df = cat_data_dict(csv, solver)
		ax = plt.subplot(gs[solvers.index(solver)], sharex=ax0)

		axis.append(ax)
		ax.yaxis.set_label_position("right")
		ax.yaxis.set_major_formatter(yticks)
		ax.set_ylabel(solver)
		ax.yaxis.get_major_ticks()[0].label1.set_visible(False)

		hist_t_query(df, ax)
		plt.ylim(0, 115)
	green = mpatches.Patch(color='green', label='0-0.1s')
	cyan = mpatches.Patch(color='cyan', label='0.1-1s')
	blue = mpatches.Patch(color='blue', label='1-2s')
	red = mpatches.Patch(color='red', label='2-15s')
	yellow = mpatches.Patch(color='yellow', label='15-30s')
	black = mpatches.Patch(color='black', label='>30s')
	axis[0].legend(handles=[green, cyan, blue, red, yellow, black], bbox_to_anchor=(0.5, 1.55),
			   loc='upper center', ncol=3)

# count queries processed within layers
def count_layered(dir, axis):
	csv = glob.glob(os.path.join(dir, '*.csv'))
	df = sio.cat_data_dict(csv, 'ppbvf')

	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)
	axis.yaxis.set_major_formatter(yticks)

	all = df.count()
	og = df[df <= 15.0].count()
	# layer1
	pd.DataFrame(og / all * 100).plot(kind='bar', ax=axis, color='skyblue', rot=-45)
	# layer2
	pd.DataFrame((all -og) / all * 100).plot.bar(bottom=og/all*100, ax=axis, color='gold', rot=-45)

	layer1 = mpatches.Patch(color='skyblue', label='layer 1')
	layer2 = mpatches.Patch(color='gold', label='layer 2')
	axis.legend(handles=[layer1, layer2], loc='upper right', bbox_to_anchor=(1.0, 1.0))


# TODO: ajdust width, gap and labels
# count queries processed in pre-processing
def count_pre(case, axis):
	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)
	axis.yaxis.set_major_formatter(yticks)

	for path, dirs, files in os.walk(case):
		X = np.linspace(1, len(dirs) / 2, len(dirs))
		X = [int(x) for x in X]
		for dir in dirs:
			project = os.path.join(path, dir)
			all = len(glob.glob(project + '/*.smt2'))
			# need after-processing
			second = len(glob.glob(project + '/*.cnf'))
			x = X[dirs.index(dir)]

			plt.bar(left=x, height=all - second, xlabel=dir,  width=0.2, color='skyblue')
			plt.bar(left=x, height=second, width=0.2, bottom=all - second, color='gold')

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


# draw time_query
def time_query():
	for dir in dirs:
		folder = dir.split('/').pop()
		time_query_project(dir)
		plt.savefig('../plots/' + folder + '-time-query', bbox_inches='tight')


# draw query-processed layers
def count_layered_all():
	gs = gridspec.GridSpec(3,1)
	gs.update(hspace=0)

	i = 0
	for dir in dirs:
		axis = plt.subplot(gs[i])
		count_layered(dir, axis)
		i += 1


# draw pre-processes query
def count_pre_all():
	gs = gridspec.GridSpec(3, 1)
	gs.update(hspace=0)

	i = 0
	for case in cases:
		axis = plt.subplot(gs[i])
		count_pre(case, axis)
		i += 1


'''
Below are usages
'''

# comb_time_all()

# comp_time_all()
# comp_time_single()
# comp_time_all_single()
# comp_time('../Out/KLEE')

# time_query_project('../Out/sage')
# time_query()

# time_solved_all()
# time_sovled(pd.read_csv('resultsample/dircolors.csv'))
# time_sovled(sio.cat_data('../Out/KLEE'))

# fig, axis = plt.subplots()
# count_layered('resultsample', axis)
# count_layered_all()

# fig, axis = plt.subplots()
# count_pre('/home/zhangysh1995/ctags', axis)
# count_pre_all()

plt.show()



