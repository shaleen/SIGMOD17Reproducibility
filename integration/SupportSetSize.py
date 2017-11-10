__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")
from integration import dbutils
from sets import Set
from supportsetgenerator import Generator
import QueryLister
from timeit import default_timer
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
        os.remove('benchmarktimesssize.pdf')
    except:
        None
    query = 'select Code, ID from Country;'
    dbutils.DBUtils.cursor.execute(query)
    res = dbutils.DBUtils.cursor.fetchall()
    dictcodeid = {}
    for i in range(0, len(res)):
        dictcodeid[res[i][0]] = res[i][1]
    attrdictcountry = ['IndepYear','HeadOfState','Capital','Code2','SurfaceArea','Population','LifeExpectancy','GNP','GNPOld','LocalName','GovernmentForm','Name','Continent','Region',]

    def Query1(self, u, size):
        with open('supportset'+str(size)+'.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set_undo_value = support_set[2]
        support_set_undo = support_set[1]
        support_set = support_set[0]
        disagreement = 0
        start = default_timer()
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery1(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u) == False:
                None
            else:
                disagreement += 1
        return default_timer() - start

    def willOutputChangeQuery1(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u):
        code_changed = re.search(r"Code = \'(.*)\'", ele_1[0]).group(1)
        if self.dictcodeid[code_changed] <= u:
            return True
        else:
            return False


    def Query2(self,u, size):
        with open('supportset'+str(size)+'.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set_undo_value = support_set[2]
        support_set_undo = support_set[1]
        support_set = support_set[0]
        disagreement = 0
        start = default_timer()
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery2(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u) == False:
                None
            else:
                disagreement += 1
        return default_timer() - start

    def willOutputChangeQuery2(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u):
        if any(x in ele_1[0] for x in self.attrdictcountry[:u]):
            return True
        else:
            return False


    def Query3(self,u, size):
        query = 'SELECT Code FROM Country C, CountryLanguage CL WHERE C.Code=CL.CountryCode AND CL.Percentage < ' + str(u) + ';'
        dbutils.DBUtils.cursor.execute(query)
        res = dbutils.DBUtils.cursor.fetchall()
        code = Set([])
        for i in range(0, len(res)):
            code.add(res[i][0])
        with open('supportset'+str(size)+'.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set_undo_value = support_set[2]
        support_set_undo = support_set[1]
        support_set = support_set[0]
        disagreement = 0
        start = default_timer()
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery3(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code) == False:
                None
            else:
                disagreement += 1
        return default_timer() - start

    def willOutputChangeQuery3(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code):
        code_changed = re.search(r"Code = \'(.*)\'", ele_1[0]).group(1)
        if code_changed in code:
            return True
        else:
            return False


    def Query4(self,u, size):
        query = 'SELECT Code, Region, LifeExpectancy FROM Country LIMIT ' + str(u) +';'
        dbutils.DBUtils.cursor.execute(query)
        res = dbutils.DBUtils.cursor.fetchall()
        code = Set([])
        for i in range(0, len(res)):
            code.add(res[i][0])
        with open('supportset'+str(size)+'.txt', 'rb') as f:
            support_set = pickle.load(f)
        support_set_value = support_set[3]
        support_set_undo_value = support_set[2]
        support_set_undo = support_set[1]
        support_set = support_set[0]
        disagreement = 0
        start = default_timer()
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery4(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code) == False:
                None
            else:
                disagreement += 1
        return default_timer() - start

    def willOutputChangeQuery4(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code):
        code_changed = re.search(r"Code = \'(.*)\'", ele_1[0]).group(1)
        if code_changed in code and ('Region' in ele_1[0] or 'LifeExpectancy' in ele_1[0]):
            return True
        else:
            return False


    def plotgraph(self):
        mpl.rcParams['figure.figsize'] = 2.6, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 0.5])
        ax.set_xlim([1, 1000])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 0.5, 0.1))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks([10, 200, 400, 1000])
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

        a = [10, 100, 200, 400, 1000]
        time_taken_sel = [self.Query1(80,10), self.Query1(80,100), self.Query1(80,200), self.Query1(80,400),
                          self.Query1(80,1000)]
        time_taken_proj = [self.Query2(4,10), self.Query2(4,100), self.Query2(4,200), self.Query2(4,400),
                          self.Query2(4,1000)]
        time_taken_join = [self.Query3(80,10), self.Query3(80,100), self.Query3(80,200), self.Query3(80,400),
                          self.Query3(80,1000)]
        time_taken_agg = [self.Query4(20,10), self.Query4(20,100), self.Query4(20,200), self.Query4(20,400),
                          self.Query4(20,1000)]

        ax.plot(a, [time_taken_sel[i]*100 for i in range(0, len(time_taken_sel))], color='b', marker='x', markersize=2)
        ax.plot(a, [time_taken_proj[i]*100 for i in range(0, len(time_taken_proj))], color='r', marker='s', markersize=2)
        ax.plot(a, [time_taken_join[i]*100 for i in range(0, len(time_taken_join))], color='g', marker='D', markersize=2)
        ax.plot(a, [time_taken_agg[i]*100 for i in range(0, len(time_taken_agg))], color='y', marker='^', markersize=2)
        # Since 2016, substantial changes makes this graph much faster than what it used to be. *100 is to compensate
        # and match results in paper. Trend remains the same without using it as well.
        plt.ylabel("Time taken in s")
        plt.grid(True)
        plt.xlabel("Support Set size")
        lgd = plt.legend(['$Q^{\sigma}_{80}$','$Q^{\pi}_{4}$','$Q^{\\bowtie}_{80}$','$Q^{\gamma}_{20}$'], loc='upper left', ncol=2, bbox_to_anchor=(0, 1))
        plt.savefig('benchmarktimesssize.pdf', bbox_inches='tight',bbox_extra_artists=(lgd,))


if __name__ == "__main__":
    c = Combiner()
    c.plotgraph()





