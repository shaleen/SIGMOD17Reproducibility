__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from constants import pricing_country
from integration import Pricer
from integration import QueryLister
from supportsetgenerator import Generator
import pickle
import os,re
from timeit import default_timer
from integration import dbutils
from sets import Set
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl
class Combiner:

    d = dbutils.DBUtils()
    g = Generator.Generator()
    q = QueryLister.Query()
    query = 'select Code, ID from Country;'
    dbutils.DBUtils.cursor.execute(query)
    res = dbutils.DBUtils.cursor.fetchall()
    dictcodeid = {}
    for i in range(0, len(res)):
        dictcodeid[res[i][0]] = res[i][1]
    attrdictcountry = ['IndepYear','HeadOfState','Capital','Code2','SurfaceArea','Population','LifeExpectancy','GNP','GNPOld','LocalName','GovernmentForm','Name','Continent','Region',]

    def executeProc(self, query_start, query_end, restore_countryview, use_which_query, clean_lpqueries=False):
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        if clean_lpqueries == True:
            dbutils.DBUtils.cursor.execute('update LPQueries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute("call ExecuteQueries(" + str(query_start) + ", " + str(query_end) + ", " \
                                       + str(self.d.no_of_elements_in_support_set()) + ", " + str(restore_countryview) + ", " + str(use_which_query) +")")
        dbutils.DBUtils.cursor.fetchall()

    def endToEndProcessing(self):
        for i in range(0, len(pricing_country.support_count)):
            labels = []
            y_plots = []
            for j in range(0, len(pricing_country.pricing_functions)):
                m = getattr(Pricer, pricing_country.pricing_functions[j])
                y_plots.append(m())
                labels.append(str(pricing_country.pricing_functions[j]))
        return y_plots

    def insertintodb(self):
        self.q.populateQueryTable()
        with open('supportset1000random.txt', 'rb') as f:
            support_set = pickle.load(f)
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call clearUpdateQuery()')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[0])
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UndoUpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[1])
        dbutils.DBUtils.cursor.fetchall()

    def generatesupportset(self):
        try:
            os.remove('supportset1000random.txt')
        except:
            None
        support_set = c.g.generateSupportSet(None, 1000)
        with open('supportset1000random.txt', 'wb') as f:
            pickle.dump(support_set, f)

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
        return float(disagreement)*100/size

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
        for i in range(0, len(support_set)):
            ele_1 = support_set[i]
            ele_undo_1 = support_set_undo[i]
            ele_undo_1_value = support_set_undo_value[i]
            ele_1_value = support_set_value[i]
            if self.willOutputChangeQuery3(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code) == False:
                None
            else:
                disagreement += 1
        return float(disagreement)*100/size

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
        return float(disagreement)*100/size

    def willOutputChangeQuery4(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, u, code):
        code_changed = re.search(r"Code = \'(.*)\'", ele_1[0]).group(1)
        if code_changed in code and ('Region' in ele_1[0] or 'LifeExpectancy' in ele_1[0]):
            return True
        else:
            return False

    def benchsel(self):
        mpl.rcParams['figure.figsize'] = 2.5, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 105])
        ax.set_xlim([1, 240])
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

        a = [math.pow(2,x) for x in range(0,8)]
        a.append(239)

        pricesel = self.endToEndProcessing()

        ax.plot(a, [y for y in pricesel[0][:9]], color='b', marker='x', markersize=2)
        ax.plot(a, [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
        ax.plot(a, [y for y in pricesel[2][:9]], color='g', marker='D', markersize=2)
        ax.plot(a, [y for y in pricesel[3][:9]], color='y', marker='^', markersize=2)
        ax.plot(a, [y for y in pricesel[4][:9]], color='khaki', marker='>', markersize=2)
        ax.plot(a, [y for y in pricesel[5][:9]], color='chocolate', marker='+', markersize=2)
        ax.plot(a, [y for y in pricesel[6][:9]], color='firebrick', marker='p', markersize=2)
        ax.plot(a, [y for y in pricesel[7][:9]], color='fuchsia', marker='<', markersize=2)
        plt.ylabel("Price")
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\sigma}_u$")
        lgd = plt.legend(['disagreementCount - nbrs', 'TsallisEntropy - nbrs',' Shannon Entropy - nbrs',  'Information Gain - nbrs',
                         'disagreementCount - uniform', 'TsallisEntropy - uniform',' Shannon Entropy - uniform',  'Information Gain - uniform', 'Random coverage - nbrs', 'Ideal price'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
        plt.savefig('benchmarkselect.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')


    def benchproj(self):
        mpl.rcParams['figure.figsize'] = 2.5, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 105])
        ax.set_xlim([1, 13])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 105, 20))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks(np.arange(1,14, 1))
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
        priceproj = self.endToEndProcessing()
        ax.plot([x for x in range(1,14)], [y for y in priceproj[0][9:22]], color='b', marker='x', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[1][9:22]], color='r', marker='s', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[2][9:22]], color='g', marker='D', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[3][9:22]], color='y', marker='^', markersize=2)

        ax.plot([x for x in range(1,14)], [y for y in priceproj[4][9:22]], color='khaki', marker='>', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[5][9:22]], color='chocolate', marker='+', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[6][9:22]], color='firebrick', marker='p', markersize=2)
        ax.plot([x for x in range(1,14)], [y for y in priceproj[7][9:22]], color='fuchsia', marker='<', markersize=2)
        #ax.plot([x for x in range(1,14)], [y for y in priceprojdprime[0][:13]], color='peru', marker='v', markersize=2)
        #ax.plot([x for x in range(1,14)], idealproj, color='m', marker='h', markersize=2)
        #plt.ylabel("Price")
        handles,labels = ax.get_legend_handles_labels()
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\pi}_u$")
        lgd = plt.legend(['coverage - nbrs', 'q-entropy - nbrs',' shannon entropy - nbrs',  'uniform info gain - nbrs',
                          'coverage - uniform', 'q-entropy - uniform',' shannon entropy - uniform',  'uniform info gain - uniform'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
        plt.savefig('benchmarkproject',  bbox_inches='tight',bbox_extra_artists=(lgd,))


    def benchjoin(self):
        mpl.rcParams['figure.figsize'] = 2.7, 1.95
        plt.yscale('log')
        fig, ax = plt.subplots()
        ax.set_xscale('log')
        ax.set_ylim([0, 105])
        ax.yaxis.set_ticks(np.arange(0, 105, 20))
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

        a = [0,0.0750,0.1550,0.3125,0.625,1.25,2.5,5,10,20,40,60,80,100]
        pricejoin = self.endToEndProcessing()
        ax.plot(a, [y for y in pricejoin[0][22:36]], color='b', marker='x', markersize=2)
        ax.plot(a, [y for y in pricejoin[1][22:36]], color='r', marker='s', markersize=2)
        ax.plot(a, [y for y in pricejoin[2][22:36]], color='g', marker='D', markersize=2)
        ax.plot(a, [y for y in pricejoin[3][22:36]], color='y', marker='^', markersize=2)
        ax.plot(a, [y for y in pricejoin[4][22:36]], color='khaki', marker='>', markersize=2)
        ax.plot(a, [y for y in pricejoin[5][22:36]], color='chocolate', marker='+', markersize=2)
        ax.plot(a, [y for y in pricejoin[6][22:36]], color='firebrick', marker='p', markersize=2)
        ax.plot(a, [y for y in pricejoin[7][22:36]], color='fuchsia', marker='<', markersize=2)
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\\bowtie}_u$")
        lgd = plt.legend(['disagreementCount - nbrs', 'TsallisEntropy - nbrs',' Shannon Entropy - nbrs',  'Information Gain - nbrs',
                          'disagreementCount - uniform', 'TsallisEntropy - uniform',' Shannon Entropy - uniform',  'Information Gain - uniform'], loc='lower right', ncol=2, bbox_to_anchor=(0, 1))
        plt.savefig('benchmarkjoin', bbox_inches='tight',bbox_extra_artists=(lgd,))


    def benchgrp(self):
        mpl.rcParams['figure.figsize'] = 2.5, 1.95
        fig, ax = plt.subplots()
        ax.set_ylim([0, 105])
        ax.set_xlim([4, 25])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 105, 20))
        #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
        ax.xaxis.set_ticks([5,10,15,20,25])
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
        a = [5,10,15,20,25]
        pricegrp = self.endToEndProcessing()
        ax.plot(a, [y for y in pricegrp[0][36:41]], color='b', marker='x', markersize=2)
        ax.plot(a, [y for y in pricegrp[1][36:41]], color='r', marker='s', markersize=2)
        ax.plot(a, [y for y in pricegrp[2][36:41]], color='g', marker='D', markersize=2)
        ax.plot(a, [y for y in pricegrp[3][36:41]], color='y', marker='^', markersize=2)
        ax.plot(a, [y for y in pricegrp[4][36:41]], color='khaki', marker='>', markersize=2)
        ax.plot(a, [y for y in pricegrp[5][36:41]], color='chocolate', marker='+', markersize=2)
        ax.plot(a, [y for y in pricegrp[6][36:41]], color='firebrick', marker='p', markersize=2)
        ax.plot(a, [y for y in pricegrp[7][36:41]], color='fuchsia', marker='<', markersize=2)
        plt.grid(True)
        plt.xlabel("$u$ parameter in $Q^{\gamma}_u$")
        plt.savefig('benchmarkgroup', bbox_inches='tight')





if __name__ == "__main__":
    c = Combiner()
    c.benchsel()
    c.benchproj()
    c.benchjoin()
    c.benchgrp()