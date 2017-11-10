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
    attrdictcountry = ['IndepYear','HeadOfState','Capital','Code2','SurfaceArea','Population','LifeExpectancy','GNP','GNPOld','LocalName','GovernmentForm','Name','Continent','Region',]
    try:
        os.remove('benchmarkprojectsupportsize.pdf')
    except OSError:
        pass
    def Query1(self, u, size):
        with open('supportset'+str(size)+'.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set_undo_value = support_set[2]
        support_set_undo = support_set[1]
        support_set = support_set[0]
        disagreement = 0
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery1(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u) == False:
                None
            else:
                disagreement += 1
        return float(disagreement)*100/size

    def willOutputChangeQuery1(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u):
        if any(x in ele_1[0] for x in self.attrdictcountry[:u]):
            return True
        else:
            return False

    def plotgraph(self):
        mpl.rcParams['figure.figsize'] = 2.5, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 105])
        ax.set_xlim([1, 13])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 105, 20))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks(np.arange(1, 14, 1))
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

        idealproj = [100/13, 200/13,300/13,400/13,500/13, 600/13, 700/13, 800/13, 900/13, 1000/13, 1100/13, 1200/13, 100]
        disagproj10 = [self.Query1(1,10), self.Query1(2,10), self.Query1(3,10), self.Query1(4,10), self.Query1(5,10)
                       , self.Query1(6,10), self.Query1(7,10), self.Query1(8,10), self.Query1(9,10), self.Query1(10,10)
                       , self.Query1(11,10), self.Query1(12,10), self.Query1(13,10)]
        disagproj100 = [self.Query1(1,100), self.Query1(2,100), self.Query1(3,100), self.Query1(4,100), self.Query1(5,100)
                       , self.Query1(6,100), self.Query1(7,100), self.Query1(8,100), self.Query1(9,100), self.Query1(10,100)
                       , self.Query1(11,100), self.Query1(12,100), self.Query1(13,100)]
        disagproj1000 = [self.Query1(1,1000), self.Query1(2,1000), self.Query1(3,1000), self.Query1(4,1000), self.Query1(5,1000)
                       , self.Query1(6,1000), self.Query1(7,1000), self.Query1(8,1000), self.Query1(9,1000), self.Query1(10,1000)
                       , self.Query1(11,1000), self.Query1(12,1000), self.Query1(13,1000)]
        ax.plot([x for x in range(1,14)],disagproj10 , color='b', marker='x', markersize=2)
        ax.plot([x for x in range(1,14)], disagproj100, color='r', marker='s', markersize=2)
        ax.plot([x for x in range(1,14)],disagproj1000 , color='g', marker='8', markersize=2)
        ax.plot([x for x in range(1,14)], idealproj, color='m', marker='v', markersize=2)
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\pi}_u$")
        lgd = plt.legend(['10','100','1000','Ideal price'], loc='lower right', ncol=1, bbox_to_anchor=(1, 0),prop={'size':6})
        plt.savefig('benchmarkprojectsupportsize.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == "__main__":
    c = Combiner()
    c.plotgraph()




