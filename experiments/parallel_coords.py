__author__ = 'shaleen'


import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas.tools.plotting import parallel_coordinates
from matplotlib import rc_file
rc_file('matplotlibrc-singlecolumn')

mpl.rcParams['figure.figsize'] = 3.5, 2
mpl.rcParams['axes.labelsize'] = 5
mpl.rcParams['ytick.labelsize'] = 5
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['xtick.major.pad']='8'
data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/bucket', sep=',')
data = data.drop(labels='  ring of D', axis=1)
parallel_coordinates(data, 'name')
ax = plt.gca()
ax.legend_ = None
plt.ylabel('Price out of 100')
plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_bucket.pdf')

# plt.clf()
#
# data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/aps', sep=',')
# data = data.drop(labels='  ring of D', axis=1)
# parallel_coordinates(data, 'name')
# ax = plt.gca()
# ax.legend_ = None
# plt.ylabel('Price out of 100')
# plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_aps.pdf')

# plt.clf()
#
# data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/tsallis', sep=',')
# data = data.drop(labels='  ring of D', axis=1)
# parallel_coordinates(data, 'name')
# ax = plt.gca()
# ax.legend_ = None
# plt.ylabel('Price out of 100')
# plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_tsallis.pdf')

plt.clf()

data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/disagreement', sep=',')
data = data.drop(labels='  ring of D', axis=1)
parallel_coordinates(data, 'name')
ax = plt.gca()
ax.legend_ = None
plt.ylabel('Price out of 100')
plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_disagreement.pdf')

plt.clf()

data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/random', sep=',')
parallel_coordinates(data, 'name')
ax = plt.gca()
ax.legend_ = None
plt.ylabel('Price out of 100')
plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_random.pdf')

plt.clf()

data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/neighborsofD', sep=',')
parallel_coordinates(data, 'name')
ax = plt.gca()
ax.legend_ = None
plt.ylabel('Price out of 100')
plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_neighborsofD.pdf')

# plt.clf()
#
# data = pandas.read_csv(r'/Users/shaleen/Documents/UW-Madison/pricing-sim.git/trunk/charts/neighborsofDprime', sep=',')
# parallel_coordinates(data, 'name')
# ax = plt.gca()
# ax.legend_ = None
# plt.ylabel('Price out of 100')
# plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/parallel_coord_neighborsofDprime.pdf')