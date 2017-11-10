__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")
from supportsetgeneratorssb import Generator
from integration_ssb import QueryLister
from integration_ssb import dbutils
import re
from timeit import default_timer
import pickle
from sets import Set
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 3.5, 1.95
import numpy as np
import random

class Combiner:
    g = Generator.Generator()
    q = QueryLister.Query()

    support_set = None #g.generateSupportSet(None, pricing_ssb.support_count[0])
    print "loading support set"
    with open('supportsetq11.txt', 'rb') as f:
        support_set = pickle.load(f)
        #pickle.dump(support_set, f)
    print "loaded support set"
    support_set_pk = support_set[4]
    support_set_value = support_set[3]
    support_set_undo_value = support_set[2]
    support_set_undo = support_set[1]
    support_set = support_set[0]
    parameters = None
    allqueries = q.generateQueriesNonDiscretized()
    queries = len(allqueries)
    text = None
    entropyplots = None
    analyticalentropy = None
    tsallis = None
    print "cleaning db utils"
    print "cleaned db utils"
    countif = 0
    countelse = 0
    landarr = Set([])

    def Query1(self,d_year, lo_discountlow, lo_discounthigh, lo_quantity):
        query1 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity < ' + str(lo_quantity) + ';'
        query2 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year != ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity < ' + str(lo_quantity) + ';'
        query3 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and (lo_discount < ' + str(lo_discountlow) + ' or lo_discount > ' + str(lo_discounthigh) + ') and lo_quantity < ' + str(lo_quantity) + ';'
        query4 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity >= ' + str(lo_quantity) + ';'
        print "starting query execution"
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        count = 0
        pkinout = Set([])
        for i in range(0, len(res)):
            pkinout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        pk2inout = Set([])
        for i in range(0, len(res)):
            pk2inout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        pk3inout = Set([])
        for i in range(0, len(res)):
            pk3inout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        pk4inout = Set([])
        for i in range(0, len(res)):
            pk4inout.add(res[i][0])
        i = 0
        countnohistory=0
        counthistory=0
        supportsetsize = 0
        start = default_timer()
        print "Started"
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            ele_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i+1]
                ele_2_value = self.support_set_value[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i]
            if ('lineorder_view' in ele_1[0]):
                supportsetsize += 1
            if self.willOutputChangeQuery1(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           code_changed_1, code_changed_2,pkinout ,pk2inout, pk3inout, pk4inout,
                                           d_year, lo_discountlow, lo_discounthigh, lo_quantity) == False:
                None
            else:
                count = count + 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        print "Query 1 : ", count
        print "time : ", default_timer() - start
        return [ default_timer() - start, float(counthistory)/supportsetsize, float(countnohistory)/supportsetsize]

    def willOutputChangeQuery1(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                               code_changed_1, code_changed_2, pkinout, pk2inout, pk3inout, pk4inout,
                               d_year, lo_discountlow, lo_discounthigh, lo_quantity):
        if ('lineorder_view' not in ele_1[0]):
            return False
        if ele_2 == None:
            if code_changed_1[0] in pkinout:
                if 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0] and not str(ele_1_value).startswith(str(d_year)):
                    return True
                if 'SET lo_quantity' in ele_1[0] and int(ele_1_value) >= lo_quantity:
                    return True
                if 'SET lo_discount' in ele_1[0] and (int(ele_1_value) > lo_discounthigh or int(ele_1_value) < 1):
                    return True
            else:
                if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value).startswith(str(d_year)) and code_changed_1[0] in pk2inout:
                    return True
                if 'SET lo_discount' in ele_1[0] and int(ele_1_value) < lo_discounthigh and int(ele_1_value) > lo_discountlow and code_changed_1[0] in pk3inout:
                    return True
                if 'SET lo_quantity' in ele_1[0] and int(ele_1_value) < lo_quantity and code_changed_1[0] in pk4inout:
                    return True
        else:
            if code_changed_1[0] not in pkinout and code_changed_2[0] not in pkinout:
                if 'SET lo_discount' in ele_1[0]:
                    if code_changed_1[0] in pk3inout:
                        if code_changed_2[0] not in pk3inout:
                            if ele_1_value < lo_discounthigh and ele_1_value > lo_discountlow:
                                return True
                    else:
                        if code_changed_2[0] in pk3inout:
                            if ele_2_value < lo_discounthigh and ele_2_value > lo_discountlow:
                                return True
                if 'SET lo_quantity' in ele_1[0]:
                    if code_changed_1[0] in pk4inout:
                        if code_changed_2[0] not in pk4inout:
                            if ele_1_value < lo_quantity:
                                return True
                    else:
                        if code_changed_2[0] in pk4inout:
                            if ele_2_value < lo_quantity:
                                return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if code_changed_1[0] in pk2inout:
                        if code_changed_2[0] not in pk2inout:
                            if str(ele_1_value).startswith(str(d_year)):
                                return True
                    else:
                        if code_changed_2[0] in pk2inout:
                            if str(ele_2_value).startswith(str(d_year)):
                                return True
            else:
                if 'SET lo_discount' in ele_1[0] or 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if (not str(ele_1_value).startswith(str(d_year)) or not str(ele_2_value).startswith(str(d_year))):
                        return True
                    else:
                        if code_changed_1[0] in pk2inout:
                            if code_changed_2[0] not in pk2inout:
                                if str(ele_1_value).startswith(str(d_year)):
                                    return True
                        else:
                            if code_changed_2[0] in pk2inout:
                                if str(ele_2_value).startswith(str(d_year)):
                                    return True
                if 'SET lo_quantity' in ele_1[0]:
                    if (ele_1_value >= lo_quantity or ele_2_value >= lo_quantity):
                        return True
                    else:
                        if code_changed_1[0] in pk2inout:
                            if code_changed_2[0] not in pk2inout:
                                if ele_1_value < lo_quantity:
                                    return True
                        else:
                            if code_changed_2[0] in pk2inout:
                                if ele_2_value < lo_quantity:
                                    return True
        return False


    def dishistoryq1(self):
        fig, ax = plt.subplots()
        mpl.rcParams['figure.figsize'] = 2.1, 1.95
        ax.set_ylim([0, 15])
        ax.set_xlim([0, 26])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 15, 5))
        #ax.yaxis.set_ticks(np.arange(0, 40, 1), minor=False)
        ax.xaxis.set_ticks(np.arange(0,26, 5))
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

        ssbcumprice = []
        ssbcumpricesavings = []
        runningcumprice = 0
        runningcumsavings = 0
        for i in range(1,26):
            year = random.randint(1992, 1998)
            dis_hi = random.uniform(0,10)
            dis_low = random.uniform(float(dis_hi)/2, dis_hi)
            quantity = random.randint(1,50)
            print year, dis_hi, dis_low, quantity
            output = self.Query1(year,dis_low, dis_hi, quantity)
            runningcumprice += output[2]
            runningcumsavings += output[1]
            print runningcumprice, runningcumsavings
            ssbcumprice.append(runningcumprice*200) #scaling up prices by a fixed factor is arbitrage free
            ssbcumpricesavings.append(runningcumsavings*200)

        ax.plot([x for x in range(1,26)], ssbcumprice, color='b', marker='>', markersize=2)
        ax.plot([x for x in range(1,26)], ssbcumpricesavings, color='r', marker='s', markersize=2)
        plt.ylabel("Price")
        plt.xlabel("Query 1.1")
        lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
        plt.savefig('ssbq11.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')



if __name__ == "__main__":
    c = Combiner()
    c.dishistoryq1()
