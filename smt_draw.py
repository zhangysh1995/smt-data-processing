import pandas as pd
import smt_stat as stat
import matplotlib.style
# TODO: plotting styles
matplotlib.style.use('seaborn-paper')
# matplotlib.style.use('ggplot')

# setup plt
# fig, ax1 = plt.subplots()
ticks = [0.1, 0.5, 1.0, 2.0]
width=0.2

# stacked distribution of query
def hist_query_all(data, ax):
	df = pd.DataFrame(data)
	draw_hist_query(df, ax)


# def hist_query(data, solver, ax):
# 	solver_data = pd.DataFrame(data).as_matrix(columns=[solver])
# 	draw_hist_query(pd.DataFrame(solver_data), ax)


def draw_hist_query(df, ax):
	count = []
	for i in range(len(ticks)):
		count.append(df[df < ticks[i]].count())
		color = stat.colors[i]
		if i == 0:
			count[i].plot.bar(ax=ax, color=color, width=width, position=0)
		else:
			(count[i] - count[i - 1]).plot.bar(bottom=count[i - 1],
											   ax=ax, color=color, width=width, position=0)


# TODO: fix bug-> empty bottom when first tick is `zero`
# stacked distribution of time
def hist_time_all(data, ax):
	df = pd.DataFrame(data)
	draw_hist_time(df, ax)


# def hist_time(data, solver, ax):
# 	solver_data = pd.DataFrame(data).as_matrix(columns=[solver])
# 	draw_hist_time(pd.DataFrame(solver_data), ax)


def draw_hist_time(df, ax):
	time = []
	for i in range(len(ticks)):
		time.append(df[df < ticks[i]].sum())
		color = stat.colors[i]
		if i == 0:
			# print(time[i])
			time[i].plot.bar(ax=ax, color=color, width=width, position=1)
		else:
			(time[i] - time[i - 1]).plot.bar(bottom=time[i - 1],
											 ax=ax, color=color, width=width, position=1)


# time vs. sovled
# TODO: make it pretty
def time_sovled(data):
	df = pd.DataFrame(data)
	df[df < 30].cumsum().plot()


'''
draw combined graph of query types
and corresponding running time
'''
def hist_t_query_all(data, ax):
	hist_query_all(data, ax)
	hist_time_all(data, ax)


def hist_t_query(data, ax):
	draw_hist_query(data, ax)
	draw_hist_time(data,ax)
