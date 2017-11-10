__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")
from supportsetgenerator import Generator
import QueryLister
import numpy as np
import re
import pickle
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 3.5, 1.95

class Combiner:

    g = Generator.Generator()
    q = QueryLister.Query()
    try:
        os.remove('benchmarkcellswapratio.pdf')
    except:
        None

    def Query1(self, size):
        with open('supportsetswap2'+str(size)+'1000.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set = support_set[0]
        disagreement = 0
        count = 0
        i = 0
        while (i < len(support_set)):
            ele_1 = support_set[i]
            if  i != len(support_set)-1 and support_set[i][1] == support_set[i+1][1]:
                i = i + 2
                count +=1
            else:
                i = i + 1
                if 'Population' in ele_1[0]:
                    disagreement += 1
        print "count:", count, disagreement
        return float(disagreement)*100/10000

    def Query2(self, size):
        with open('supportsetswap'+str(size)+'1000.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set = support_set[0]
        disagreement = 0
        i=0
        while (i < len(support_set)):
            ele_1 = support_set[i]
            ele_1_value = support_set_value[i]
            if  i != len(support_set)-1 and  support_set[i][1] == support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
                if 'Population' in ele_1[0] and ele_1_value > 2000000000:
                    disagreement += 1
        return float(disagreement)*100/1000


    def plotgraph(self):
        mpl.rcParams['figure.figsize'] = 2.5, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([-1, 25])
        ax.set_xlim([0, 1])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 25, 5))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
        ax.tick_params(
                axis='x',          # changes apply to the x-axis
                which='major',      # both major and minor ticks are affected
                bottom='on',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                direction='out',
                labelbottom='on') # labels along the bottom edge are off

        ax.tick_params(
                axis='y',
                which='major',
                left='on',
                right='off',
                direction='out')

        ax.plot([0, 0.25, 0.5, 0.75, 1], [self.Query1(0), self.Query1(25), self.Query1(50),self.Query1(75),self.Query1(100)], color='b', marker='x', markersize=2)
        ax.plot([0, 0.25, 0.5, 0.75, 1], [self.Query2(0), self.Query2(25), self.Query2(50),self.Query2(75),self.Query2(100)], color='m', marker='h', markersize=2)

        plt.grid(True)
        plt.xlabel("fraction of swap updates")
        lgd = plt.legend(['$Q^{r}_1$', '$Q^{r}_2$'], loc='upper left', ncol=4, bbox_to_anchor=(0, 1))
        plt.savefig('benchmarkcellswapratio.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == "__main__":
    c = Combiner()
    c.plotgraph()







