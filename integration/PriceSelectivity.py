__author__ = 'shaleen'
from integration import dbutils
from supportsetgenerator import Generator
from charts import Charting
import QueryLister
import os
import re
import pickle
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl

mpl.rcParams['figure.figsize'] = 3.5, 1.95

class Combiner:

    g = Generator.Generator()
    q = QueryLister.Query()
    c = Charting.Charts()
    query = 'select Code, ID from Country;'
    dbutils.DBUtils.cursor.execute(query)
    res = dbutils.DBUtils.cursor.fetchall()
    dictcodeid = {}
    for i in range(0, len(res)):
        dictcodeid[res[i][0]] = res[i][1]
    os.remove('benchmarkselectsupportsize.pdf')
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
        code_changed = re.search(r"Code = \'(.*)\'", ele_1[0]).group(1)
        if self.dictcodeid[code_changed] <= u:
            return True
        else:
            return False

    def plotgraph(self):
        mpl.rcParams['figure.figsize'] = 2.8, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 105])
        ax.set_xlim([1, 239])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 105, 20))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks([1,32,64,128,239])
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
        idealsel = [0, 100/239,300/239,700/239,1500/239,3100/239,6300/239,12700/239, 100]
        disagsel10 = [self.Query1(1,10),self.Query1(2,10),self.Query1(4,10),self.Query1(8,10),self.Query1(16,10),
                      self.Query1(32,10),self.Query1(64,10),self.Query1(128,10),self.Query1(239,10)]
        disagsel100 = [self.Query1(1,100),self.Query1(2,100),self.Query1(4,100),self.Query1(8,100),self.Query1(16,100),
                      self.Query1(32,100),self.Query1(64,100),self.Query1(128,100),self.Query1(239,100)]
        disagsel1000 = [self.Query1(1,1000),self.Query1(2,1000),self.Query1(4,1000),self.Query1(8,1000),self.Query1(16,1000),
                      self.Query1(32,1000),self.Query1(64,1000),self.Query1(128,1000),self.Query1(239,1000)]
        a = [math.pow(2,x) for x in range(0,8)]
        a.append(239)
        ax.plot(a, disagsel10, color='b', marker='x', markersize=2)
        ax.plot(a, disagsel100, color='r', marker='s', markersize=2)
        ax.plot(a, disagsel1000, color='g', marker='8', markersize=2)
        ax.plot(a, idealsel, color='m', marker='v', markersize=2)
        plt.ylabel("Price")
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\sigma}_u$")
        lgd = plt.legend(['10','100','1000', 'Ideal price'], loc='lower right', ncol=1, bbox_to_anchor=(1, 0),prop={'size':6})
        plt.savefig('benchmarkselectsupportsize.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == "__main__":
    c = Combiner()
    c.plotgraph()




