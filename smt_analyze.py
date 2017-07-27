import pandas as pd

'''
Usage:
import smt_analyze as sal
'''

# Example
# data = read_data('Out/xxx.csv')
# hist_t_query(data)
# plt.show() # Remember to add this line


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
