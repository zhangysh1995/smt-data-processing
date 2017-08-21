import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches

smtbench = '/home/zhangysh1995/work/ppdev/smtbench/cmake-build-debug/smtbench '

colors = ['k', 'royalblue', 'dodgerblue', 'deepskyblue', 'lightskyblue']
# query type of a project


# calculate the feature of every query in a project folder e.g. sage
def type_dir(project):
	for path, dirs, files in os.walk(project):
		for d in dirs:
			cmd = smtbench + path + '/' + d
			print(cmd)
			with open('../Out/features.csv', 'a') as f:
				f.write(d + '\n')
				f.close()
			os.system(cmd)


# count type of queries
def count(file):
	n = np.zeros(32)
	with open('../Out/' + file + '.csv', 'r') as f:
		for line in f:
			col = 0
			for data in line.split():
				if col != 0 and col != 33:
					n[col-1] += int(data)
				col += 1

	return n


# bar of types
def draw_type(dir):
	plt.bar(range(0, 32), count(dir))
	plt.savefig('../Out/', dir.split('/').pop() + '-type.png')


# sum of types
def variable(file):
	var_list = []
	out = '../Out/' + file + '.csv'
	with open(out, 'r') as f:
		var_list.append(f.readline())

		var = 0
		for line in f:
			print(line)
			data = line.split()
			if 'smt2' in data[0]:
				var += int(data.pop())
			else:
				var_list.append(var)
				var_list.append(data[0])
				var = 0
		var_list.append(var)
	return var_list, dir


# histogram of variable
def variable_hist(file):
	dir = []
	var_list = []
	out = '../Out/' + file + '.csv'
	with open(out, 'r') as f:
		dir.append(f.readline())

		dir_list = []
		for line in f:
			data = line.split()
			if 'smt2' in data[0]:
				dir_list.append(int(data.pop()))
			else:
				dir.append(data[0])
				var_list.append(dir_list)
				dir_list = []
		var_list.append(dir_list)
	return dir, var_list


# atomic predicates hist
def atomic_hist(file):
	atomic = [1, 8, 15, 19, 22, 23, 24, 25, 26]
	dir = []
	atomic_no = []
	out = '../Out/' + file + '.csv'
	with open(out, 'r') as f:
		dir.append(f.readline())

		atomic_sum = []
		for line in f:
			data = line.split()
			if 'smt2' in data[0]:
				data = [int(d) for d in data[1:-1]]
				atomic_sum.append(sum([data[i] for i in atomic]))
			else:
				dir.append(data[0])
				atomic_no.append(atomic_sum)
				atomic_sum = []
		atomic_no.append(atomic_sum)
	return dir, atomic_no


# draw distribution of variables for one file
def var_percent(file):
	var = variable_hist(file)
	dirs, ticks = percent(var)
	# set x ticks
	plt.xticks(ticks, dirs)
	# set legend
	# plt.title('Distribution of Variable Numbers Across sage Projects')
	plt.xlabel('Applications')
	# plt.ylabel('No.')
	plt.savefig('Distribution-of-variable.png', bbox_inches='tight')


# draw distribution of variables for one file
def atomic_percent(file):
	var = atomic_hist(file)
	dirs, ticks = percent(var)
	# set x ticks
	plt.xticks(ticks, dirs)
	# set legend
	plt.xlabel('Applications')
	# plt.ylabel('No.')
	plt.savefig('Distribution-of-atomic.png', bbox_inches='tight')


# distribution of variables in a benchmark with quartiles
# actually not useful
def percent(var):
	dirs = var[0]
	var_list = var[1]
	set_style()
	# generate x position for bars
	ticks = range(len(dirs) + 1)[1:]
	# iterate each project
	for d, v, x in zip(dirs, var_list, ticks):
		window = np.linspace(0, max(v), 5)
		count = []
		all = len(v)
		# count cumulative sum with window
		for w in window:
			count.append(len(list(filter(lambda n: n <= w, v))))
		# normalize y
		count = [c / all * 100 for c in count]
		# plot the bar for one project stacked
		for i, c in enumerate(count):
			if i == 0:
				plt.bar(x, c / all * 100, color=colors[i])
			else:
				plt.bar(x, c - count[i - 1], bottom=count[i - 1], color=colors[i])

	return dirs, ticks


# set the plots styles
def set_style():
	ax = plt.subplot()
	# format y tick to percentage
	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)
	ax.yaxis.set_major_formatter(yticks)


# grasp the sum of each feature in one project respectively
def get_features(file):
	out = '../Out/' + file + '.csv'

	with open(out, 'r') as f:
		dirs = []
		dirs.append(f.readline())
		feature = np.zeros(32)
		features = []

		for line in f:
			data = line.split()
			if 'smt2' in data[0]:
				data = [int(d) for d in data[1:-1]]
				feature = [f + d for f, d in zip(feature, data)]
			else:
				dirs.append(data[0])
				features.append(feature)
				feature = np.zeros(32)
		features.append(feature)
	return dirs, features


'''
Below are function wrappers
'''


def draw_variable_hist(file):
	var = variable_hist(file)
	dir = var[0]
	var_list = var[1]

	for i, v in enumerate(var_list):
		pd.DataFrame(v).plot(kind='hist', title=dir[i])


def linearity(file):
	basic = [4, 6, 7, 12, 14]
	linear = [18, 20]
	nlinear = [5, 17, 21, 27, 28, 29, 30, 31]
	dirs, features = get_features(file)
	data = {}
	for d, f in zip(dirs, features):
		data.update({d: f})

	ticks = range(len(dirs)+1)[1:]
	set_style()
	for t, d, feature in zip(ticks, dirs, features):
		all = sum([feature[i] for i in basic + linear + nlinear])
		i = 0
		bn = [i + feature[b] for b in basic]
		i = 0
		plt.bar(t, sum(bn)/all*100, color='dodgerblue')
		ln = [i + feature[l] for l in linear]
		plt.bar(t, sum(ln)/all*100, bottom=sum(bn)/all*100, color='springgreen')
		i = 0
		nln = [i + feature[n] for n in nlinear]
		plt.bar(t, sum(nln)/all*100, bottom=(sum(bn)+sum(ln))/all*100, color='yellow')
	# set legend
	axis = plt.subplot()
	blue = mpatches.Patch(color='dodgerblue', label='Basic')
	green = mpatches.Patch(color='springgreen', label='Linear')
	yellow = mpatches.Patch(color='yellow', label='Non-linear')
	axis.legend(handles=[blue, green, yellow])
	# set x ticks
	plt.xticks(ticks, dirs)
	plt.savefig('linearity.png', bbox_inches='tight')


# ratio of euqal:inequal
def equality(file):
	inequal = [8, 15, 19, 22, 23, 24, 25, 26]
	equal = [1]
	dirs, features = get_features(file)
	data = {}
	for d, f in zip(dirs, features):
		data.update({d: f})

	ticks = range(len(dirs)+1)[1:]
	set_style()
	for t, d, feature in zip(ticks, dirs, features):
		all = sum([feature[i] for i in inequal + equal])
		iq = [i + feature[i] for i in inequal]
		plt.bar(t, sum(iq)/all*100, color='dodgerblue')
		plt.bar(t, feature[1]/all*100, bottom=sum(iq)/all*100, color='springgreen')
	# set legend
	axis = plt.subplot()
	blue = mpatches.Patch(color='dodgerblue', label='Inequality')
	green = mpatches.Patch(color='springgreen', label='Equality')
	axis.legend(handles=[blue, green])
	# set x ticks
	plt.xticks(ticks, dirs)
	plt.savefig('equality.png', bbox_inches='tight')


# a query is count as linear if it has more linear features than non-linears
def linear_set(file):
	# basic_list = [4, 6, 7, 12, 14]
	linear_list = [18, 20]
	nlinear_list = [5, 17, 21, 27, 28, 29, 30, 31]
	out = '../Out/' + file + '.csv'

	with open(out, 'r') as f:
		dirs = []
		dirs.append(f.readline())
		type = np.zeros(3)
		types = []

		for line in f:
			data = line.split()
			if 'smt2' in data[0]:
				data = [int(d) for d in data[1:-1]]
				nzero = [i for i, f in enumerate(data) if f > 0]
				if len(set.intersection(set(nzero), nlinear_list)) > 0:
					type[0] += 1
				elif len(set.intersection(set(nzero), linear_list)) > 0:
					type[1] += 1
				else:
					type[2] += 1
			else:
				dirs.append(data[0])
				types.append(type)
				type = np.zeros(3)
		types.append(type)
	return dirs, types


# similar to last
def linear_ratio(file):
	# basic_list = [4, 6, 7, 12, 14]
	linear_list = [18, 20]
	nlinear_list = [5, 17, 21, 27, 28, 29, 30, 31]
	out = '../Out/' + file + '.csv'

	with open(out, 'r') as f:
		dirs = []
		dirs.append(f.readline())
		type = np.zeros(2)
		types = []

		for line in f:
			data = line.split()
			if 'smt2' in data[0]:
				data = [int(d) for d in data[1:-1]]
				linear = sum([data[i] for i in linear_list])
				nlinear = sum([data[i] for i in nlinear_list])
				if linear > nlinear:
					type[0] += 1
				else:
					type[1] += 1
			else:
				dirs.append(data[0])
				types.append(type)
				type = np.zeros(2)
		types.append(type)
	return dirs, types


'''
Below are usages
'''

# type_dir('/home/zhangysh1995/PPBV/KLEE')
# draw_type ('/home/zhangysh1995/PPBV/KLEE')
# plt.bar(range(0, 32), count('sage'))
# variable_hist('sage')
# var_percent('sage')
atomic_percent('sage')
# get_features('sage')
# linearity('sage')
# equality('sage')
# dirs, types = linear_set('sage')
# dirs, types = linear_ratio('ppcase')

plt.show()
