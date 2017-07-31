import matplotlib.pyplot as plt
from smt_stat import solvers
import smt_analyze as sal
from smt_draw import hist_t_query

path = 'resultsample/dircolors-2017-07-28-all.csv'

index = range(len(solvers))
fig, axes = plt.subplots(nrows=4)

def multi_time_query():
	data = sal.read_data(path)
	for solver in solvers:
		bin = index[solvers.index(solver)]
		hist_t_query(data, solver, ax=axes[bin])

# def multi_time:

multi_time_query()
plt.show()

