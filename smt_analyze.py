import smt_stat as stat
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')
import pandas as pd

ticks = [0.1, 0.5, 1.0, 2.0]
data = pd.read_csv('Out/2017-07-25-all.csv')
data.head()

fig, ax1 = plt.subplots()
width=0.2

def com_time():
	df = pd.DataFrame(data.sum(axis=0))
	df.plot.bar(stacked=True)

# stacked distribution of query
def hist_query():
	df = pd.DataFrame(data)
	count = []
	for i in range(len(ticks)):
		count.append(df[df < ticks[i]].count())

	for i in range(len(ticks)):
		color = stat.colors[i]
		if i == 0:
			count[i].plot.bar(ax=ax1, color=color, width=width, position=0)
		else:
			(count[i]-count[i-1]).plot.bar(bottom=count[i-1], ax=ax1, color=color, width=width, position=0)

# stacked distribution of time
def hist_time():
	df = pd.DataFrame(data)
	time = []
	for i in range(len(ticks)):
		time.append(df[df < ticks[i]].sum())

	for i in range(len(ticks)):
		color = stat.colors[i]
		if i == 0:
			time[i].plot.bar(ax=ax1, color=color, width=width, position=1)
		else:
			(time[i] - time[i - 1]).plot.bar(bottom=time[i - 1], ax=ax1, color=color, width=width, position=1)

# draw combined graph of query types and corresponding running time
def hist_t_query():
	hist_query()
	hist_time()

plt.show()