import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
smtbench = '/home/zhangysh1995/work/ppdev/smtbench/cmake-build-debug/smtbench '

colors = ['orchid', 'dodgerblue', 'springgreen', 'yellow']
# query type of a project
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


# draw distribution of variables for one file
def var_percent(file):
	var = variable_hist(file)
	dir = var[0]
	var_list = var[1]

	ax = plt.subplot()
	# generate x position for bars
	ticks = range(len(dir)+1)[1:]
	# iterate each project
	for d, v, x in zip(dir, var_list, ticks):
		window = np.linspace(0, max(v), 4)
		count = []
		all = len(v)
		# count cumulative sum with window
		for w in window:
			count.append(len(list(filter(lambda n: n <= w, v))))
		# normalize y
		count = [c/all*100 for c in count]
		# plot the bar for one project stacked
		for i, c in enumerate(count):
			if i == 0:
				plt.bar(x, c/all*100, color=colors[i])
			else:
				plt.bar(x, c-count[i-1], bottom=count[i-1], color=colors[i])
	# format y tick to percentage
	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)
	ax.yaxis.set_major_formatter(yticks)
	# set x ticks
	plt.xticks(ticks, dir)
	# set legend
	plt.title('Distribution of Variable Numbers Across sage Projects')
	plt.xlabel('project')
	plt.ylabel('No.')

# def feature_hist(file):


'''
Below are function wrappers
'''


def draw_variable_hist(file):
	var = variable_hist(file)
	dir = var[0]
	var_list = var[1]

	for i, v in enumerate(var_list):
		pd.DataFrame(v).plot(kind='hist', title=dir[i])


# type_dir('/home/zhangysh1995/PPBV/PP-CASE')
# draw_type ('/home/zhangysh1995/PPBV/KLEE')
# plt.bar(range(0, 32), count('sage'))
# variable_hist('sage')
# var_percent('sage')
plt.show()
