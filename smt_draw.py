import pandas as pd
import smt_stat as stat

# setup plt
# fig, ax1 = plt.subplots()
ticks = [0.1, 1.0, 2.0, 15, 35]
width=0.2

# time vs. sovled
# TODO: make it pretty
def time_sovled(data):
	df = pd.DataFrame(data)
	df[df <= 30].cumsum().plot()


'''
draw combined graph of query types
and corresponding running time
'''

def hist_t_query(df, ax):
	count = []
	all = df.count(axis=0)
	time = []
	sum = df.sum(axis=0)
	rot = 45
	for i in range(len(ticks)):
		count.append((df[df < ticks[i]].count())/all*100)
		time.append((df[df < ticks[i]].sum())/sum*100)
		color = stat.colors[i]

		if i == 0:
			count[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=-0.05)
			time[i].plot(kind='bar', ax=ax, rot=rot, color=color, width=width, position=1.05)
		else:
			(count[i] - count[i - 1]).plot(kind='bar', bottom=count[i - 1],
											   ax=ax, rot=rot, color=color, width=width, position=-0.05)
			(time[i] - time[i - 1]).plot(kind='bar', bottom=time[i - 1],
								 ax=ax, rot=rot,color=color, width=width, position=1.05)