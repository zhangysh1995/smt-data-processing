import pandas as pd
import matplotlib.pyplot as plt
import smt_stat as stat
import matplotlib.style
# TODO: plotting styles
matplotlib.style.use('seaborn-paper')

# setup plt
fig, ax1 = plt.subplots()
ticks = [0, 0.1, 0.5, 1.0, 2.0]
width=0.2

# stacked distribution of query
def hist_query_all(data):
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
def hist_time_all(data):
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


# time vs. sovled
# TODO: make it pretty
def time_sovled(data):
	df = pd.DataFrame(data)
	df.cumsum().plot()

# TODO: automatic drawing/saving
'''
draw combined graph of query types
and corresponding running time
'''


def hist_t_query(data):
	hist_query_all(data)
	hist_time_all(data)


