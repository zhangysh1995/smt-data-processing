import smt_stat as stat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')
from matplotlib.ticker import FuncFormatter
import pandas as pd

'''
Usage:
import smt_analyze as sal
'''

# Example
# data = read_data('Out/xxx.csv')
# hist_t_query(data)
# plt.show() # Remember to add this line


ticks = [0.1, 0.5, 1.0, 2.0]

# setup plt
fig, ax1 = plt.subplots()
# ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
width=0.2


'''
Below are function definitions
'''

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

# stacked distribution of query
def hist_query(data):
	df = pd.DataFrame(data)
	count = []
	for i in range(len(ticks)):
		count.append(df[df < ticks[i]].count())
		color = stat.colors[i]
		if i == 0:
			count[i].plot.bar(ax=ax1, color=color, width=width, position=0)
		else:
			(count[i]-count[i-1]).plot.bar(bottom=count[i-1],
										   ax=ax1, color=color, width=width, position=0)

# stacked distribution of time
def hist_time(data):
	df = pd.DataFrame(data)
	time = []
	for i in range(len(ticks)):
		time.append(df[df < ticks[i]].sum())
		color = stat.colors[i]
		if i == 0:
			time[i].plot.bar(ax=ax1, color=color, width=width, position=1)
		else:
			(time[i] - time[i - 1]).plot.bar(bottom=time[i - 1],
											 ax=ax1, color=color, width=width, position=1)

# draw combined graph of query types
# and corresponding running time
def hist_t_query(data):
	hist_query(data)
	hist_time(data)
