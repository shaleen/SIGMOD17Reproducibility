__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")
from supportsetgeneratorssb import Generator
from integration_ssb import QueryLister
from integration_ssb import dbutils
from timeit import default_timer
import pickle
from sets import Set
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 3.5, 1.95
import numpy as np

class Combiner:
    g = Generator.Generator()
    q = QueryLister.Query()

    support_set = None
    print "loading support set"
    with open('supportsetnew99999.txt', 'rb') as f:
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
    data = [[0 for i in range(0, len(allqueries) + 1)] for j in range(100001)]
    ssbcumprice = []
    ssbcumpricesavings = []
    ssbcumtime = []
    ssbcumtimesavings = []
    runningcumprice = 0
    runningcumsavings = 0
    runningssbcumtime = 0
    runningssbcumtimesavings = 0
    naive = []
    with_sampling = []
    qt = []

    print "cleaning db utils"
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`lineorder_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`part_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`customer_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`supplier_view`;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `lineorder_view` (  `lo_orderkey` int(11) NOT NULL,  `lo_linenumber` int(11) NOT NULL,  `lo_custkey` int(11) NOT NULL,  `lo_partkey` int(11) NOT NULL,  `lo_suppkey` int(11) NOT NULL,  `lo_orderdate` int(11) NOT NULL,  `lo_orderpriority` varchar(15) NOT NULL,  `lo_shippriority` varchar(1) NOT NULL,  `lo_quantity` int(11) NOT NULL,  `lo_extendedprice` int(11) NOT NULL,  `lo_ordertotalprice` int(11) NOT NULL,  `lo_discount` int(11) NOT NULL,  `lo_revenue` int(11) NOT NULL,  `lo_supplycost` int(11) NOT NULL,  `lo_tax` int(11) NOT NULL,  `lo_commitdate` int(11) NOT NULL,  `lo_shipmode` varchar(10) NOT NULL,  `lo_pk` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`lo_pk`),  KEY `index2` (`lo_orderkey`,`lo_linenumber`,`lo_custkey`,`lo_partkey`,`lo_suppkey`,`lo_orderdate`,`lo_orderpriority`,`lo_shippriority`,`lo_quantity`,`lo_extendedprice`,`lo_ordertotalprice`,`lo_discount`,`lo_revenue`,`lo_supplycost`,`lo_tax`,`lo_commitdate`) USING BTREE) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `part_view` (  `p_partkey` int(11) NOT NULL,  `p_name` varchar(22) NOT NULL,  `p_mfgr` varchar(6) DEFAULT NULL,  `p_category` varchar(7) NOT NULL,  `p_brand1` varchar(9) NOT NULL,  `p_color` varchar(11) NOT NULL,  `p_type` varchar(25) NOT NULL,  `p_size` int(11) NOT NULL,  `p_container` varchar(10) NOT NULL,  PRIMARY KEY (`p_partkey`),  KEY `index1` (`p_name`,`p_mfgr`,`p_category`,`p_brand1`,`p_color`,`p_type`,`p_size`,`p_container`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `supplier_view` (  `s_suppkey` int(11) NOT NULL,  `s_name` varchar(25) NOT NULL,  `s_address` varchar(25) NOT NULL,  `s_city` varchar(10) NOT NULL,  `s_nation` varchar(15) NOT NULL,  `s_region` varchar(12) NOT NULL,  `s_phone` varchar(15) NOT NULL,  PRIMARY KEY (`s_suppkey`),  KEY `index2` (`s_name`,`s_address`,`s_city`,`s_nation`,`s_region`,`s_phone`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `customer_view` (  `c_custkey` int(11) NOT NULL,  `c_name` varchar(25) NOT NULL,  `c_address` varchar(25) NOT NULL,  `c_city` varchar(10) NOT NULL,  `c_nation` varchar(15) NOT NULL,  `c_region` varchar(12) NOT NULL,  `c_phone` varchar(15) NOT NULL,  `c_mktsegment` varchar(10) NOT NULL,  PRIMARY KEY (`c_custkey`),  KEY `index1` (`c_custkey`) USING BTREE,  KEY `index2` (`c_name`) USING BTREE,  KEY `index3` (`c_address`) USING BTREE,  KEY `index4` (`c_nation`) USING BTREE,  KEY `index5` (`c_nation`,`c_region`,`c_phone`,`c_mktsegment`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    print "cleaned db utils"
    countif = 0
    countelse = 0
    landarr = []

    def cleanup(self):
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`lineorder_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`part_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`customer_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `ssb`.`supplier_view`;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `lineorder_view` (  `lo_orderkey` int(11) NOT NULL,  `lo_linenumber` int(11) NOT NULL,  `lo_custkey` int(11) NOT NULL,  `lo_partkey` int(11) NOT NULL,  `lo_suppkey` int(11) NOT NULL,  `lo_orderdate` int(11) NOT NULL,  `lo_orderpriority` varchar(15) NOT NULL,  `lo_shippriority` varchar(1) NOT NULL,  `lo_quantity` int(11) NOT NULL,  `lo_extendedprice` int(11) NOT NULL,  `lo_ordertotalprice` int(11) NOT NULL,  `lo_discount` int(11) NOT NULL,  `lo_revenue` int(11) NOT NULL,  `lo_supplycost` int(11) NOT NULL,  `lo_tax` int(11) NOT NULL,  `lo_commitdate` int(11) NOT NULL,  `lo_shipmode` varchar(10) NOT NULL,  `lo_pk` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`lo_pk`),  KEY `index2` (`lo_orderkey`,`lo_linenumber`,`lo_custkey`,`lo_partkey`,`lo_suppkey`,`lo_orderdate`,`lo_orderpriority`,`lo_shippriority`,`lo_quantity`,`lo_extendedprice`,`lo_ordertotalprice`,`lo_discount`,`lo_revenue`,`lo_supplycost`,`lo_tax`,`lo_commitdate`) USING BTREE) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `part_view` (  `p_partkey` int(11) NOT NULL,  `p_name` varchar(22) NOT NULL,  `p_mfgr` varchar(6) DEFAULT NULL,  `p_category` varchar(7) NOT NULL,  `p_brand1` varchar(9) NOT NULL,  `p_color` varchar(11) NOT NULL,  `p_type` varchar(25) NOT NULL,  `p_size` int(11) NOT NULL,  `p_container` varchar(10) NOT NULL,  PRIMARY KEY (`p_partkey`),  KEY `index1` (`p_name`,`p_mfgr`,`p_category`,`p_brand1`,`p_color`,`p_type`,`p_size`,`p_container`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `supplier_view` (  `s_suppkey` int(11) NOT NULL,  `s_name` varchar(25) NOT NULL,  `s_address` varchar(25) NOT NULL,  `s_city` varchar(10) NOT NULL,  `s_nation` varchar(15) NOT NULL,  `s_region` varchar(12) NOT NULL,  `s_phone` varchar(15) NOT NULL,  PRIMARY KEY (`s_suppkey`),  KEY `index2` (`s_name`,`s_address`,`s_city`,`s_nation`,`s_region`,`s_phone`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `customer_view` (  `c_custkey` int(11) NOT NULL,  `c_name` varchar(25) NOT NULL,  `c_address` varchar(25) NOT NULL,  `c_city` varchar(10) NOT NULL,  `c_nation` varchar(15) NOT NULL,  `c_region` varchar(12) NOT NULL,  `c_phone` varchar(15) NOT NULL,  `c_mktsegment` varchar(10) NOT NULL,  PRIMARY KEY (`c_custkey`),  KEY `index1` (`c_custkey`) USING BTREE,  KEY `index2` (`c_name`) USING BTREE,  KEY `index3` (`c_address`) USING BTREE,  KEY `index4` (`c_nation`) USING BTREE,  KEY `index5` (`c_nation`,`c_region`,`c_phone`,`c_mktsegment`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;')

    def Query1(self):
        d_year = 1994
        lo_discountlow = 1
        lo_discounthigh = 10
        lo_quantity = 50
        query1 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity < ' + str(lo_quantity) + ';'
        query2 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year != ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity < ' + str(lo_quantity) + ';'
        query3 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and (lo_discount < ' + str(lo_discountlow) + ' or lo_discount > ' + str(lo_discounthigh) + ') and lo_quantity < ' + str(lo_quantity) + ';'
        query4 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_year = ' + str(d_year) + ' and lo_discount between ' + str(lo_discountlow) + ' and ' + str(lo_discounthigh) + ' and lo_quantity >= ' + str(lo_quantity) + ';'
        print "starting query execution"
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        count = 0
        pkinout = Set([])
        for i in range(0, len(res)):
            pkinout.add(res[i][0])
        endq = default_timer()
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
        timesaved = 0
        start = default_timer()
        print "Started"
        while (i < len(self.support_set)):
            current = default_timer()
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
            if self.willOutputChangeQuery1(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           code_changed_1, code_changed_2,pkinout ,pk2inout, pk3inout, pk4inout,
                                           d_year, lo_discountlow, lo_discounthigh, lo_quantity) == False:
                self.data[index][1] = 0
            else:
                self.data[index][1] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        print "Query 1 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        return [default_timer() - start, float(counthistory)/len(self.support_set), float(countnohistory)/len(self.support_set), timesaved, endq - beginq, endq - beginq]

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

    def Query12(self):
        query1 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_yearmonthnum = 199401 and lo_discount between  4 and 6 and lo_quantity between 26 and 35;'
        query2 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_yearmonthnum != 199401 and lo_discount between  4 and 6 and lo_quantity between 26 and 35;'
        query3 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_yearmonthnum = 199401 and (lo_discount <  4 or lo_discount > 6) and lo_quantity between 26 and 35;'
        query4 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_yearmonthnum = 199401 and lo_discount between  4 and 6 and (lo_quantity < 26 or lo_quantity > 35);'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
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
        start = default_timer()
        print "Started"
        countnohistory=0
        counthistory=0
        timesaved = 0
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery12(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value, pkinout,
                                           pk2inout, pk3inout, pk4inout, code_changed_1, code_changed_2) == False:
                self.data[index][1] = 0
            else:
                self.data[index][1] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        print "Query 12 : " , countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        return [default_timer() - start, float(counthistory)/len(self.support_set), float(countnohistory)/len(self.support_set), timesaved, endq - beginq, endq - beginq]

    def willOutputChangeQuery12(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value, pkinout,
                                           pk2inout, pk3inout, pk4inout, code_changed_1, code_changed_2):
        if ('lineorder_view' not in ele_1[0]):
            return False
        if ele_2 == None:
            if code_changed_1 in pkinout:
                if 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0] and (not str(ele_1_value).startswith('199401')): #static check for week num TBD
                    return True
                if 'SET lo_quantity' in ele_1[0] and (int(ele_1_value) > 35 or int(ele_1_value) < 26):
                    return True
                if 'SET lo_discount' in ele_1[0] and (int(ele_1_value) > 6 or int(ele_1_value) < 4):
                    return True
            else:
                if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value).startswith('199401') and code_changed_1 in pk2inout:
                    return True
                if 'SET lo_discount' in ele_1[0] and int(ele_1_value) < 6 and int(ele_1_value) > 4 and code_changed_1 in pk3inout:
                    return True
                if 'SET lo_quantity' in ele_1[0] and int(ele_1_value) <=35 and int(ele_1_value) >=26 and code_changed_1 in pk4inout:
                    return True
        else:
            if code_changed_1 not in pkinout and code_changed_2 not in pkinout:
                if 'SET lo_discount' in ele_1[0]:
                    if code_changed_1 in pk3inout:
                        if code_changed_2 not in pk3inout:
                            if ele_1_value < 6 and ele_1_value > 4:
                                return True
                    else:
                        if code_changed_2 in pk3inout:
                            if ele_2_value < 6 and ele_2_value > 4:
                                return True
                if 'SET lo_quantity' in ele_1[0]:
                    if code_changed_1 in pk4inout:
                        if code_changed_2 not in pk4inout:
                            if ele_1_value <= 35 and ele_1_value >= 26:
                                return True
                    else:
                        if code_changed_2 in pk4inout:
                            if ele_1_value <= 35 and ele_1_value >= 26:
                                return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if code_changed_1 in pk2inout:
                        if code_changed_2 not in pk2inout:
                            if str(ele_1_value).startswith('199401'):
                                return True
                    else:
                        if code_changed_2 in pk2inout:
                            if str(ele_2_value).startswith('199401'):
                                return True
            else:
                if 'SET lo_discount' in ele_1[0] or 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if (not str(ele_1_value).startswith('199401') or not str(ele_2_value).startswith('199401')):
                        return True
                    else:
                        if code_changed_1 in pk2inout:
                            if code_changed_2 not in pk2inout:
                                if str(ele_1_value).startswith('199401'):
                                    return True
                        else:
                            if code_changed_2 in pk2inout:
                                if str(ele_2_value).startswith('199401'):
                                    return True
                if 'SET lo_quantity' in ele_1[0]:
                    if ((ele_1_value > 35 and ele_1_value < 26) or (ele_1_value > 35 and ele_1_value < 26)):
                        return True
                    else:
                        if code_changed_1 in pk2inout:
                            if code_changed_2 not in pk2inout:
                                if ele_1_value <= 35 and ele_1_value >= 26:
                                    return True
                        else:
                            if code_changed_2 in pk2inout:
                                if ele_2_value <= 35 and ele_2_value >= 26:
                                    return True
        return False

    def Query13(self):
        query1 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear = 6 and d_year = 1994 and lo_discount between 5 and 7 and lo_quantity between 26 and 35; '
        query2 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear != 6 and d_year = 1994 and lo_discount between 5 and 7 and lo_quantity between 26 and 35; '
        query3 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear = 6 and d_year != 1994 and lo_discount between 5 and 7 and lo_quantity between 26 and 35; '
        query4 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear = 6 and d_year = 1994 and (lo_discount < 5 or lo_discount > 7) and lo_quantity between 26 and 35; '
        query5 = 'select lo_pk from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear = 6 and d_year = 1994 and lo_discount between 5 and 7 and (lo_quantity < 26 or lo_quantity > 35); '
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
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
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        pk5inout = Set([])
        for i in range(0, len(res)):
            pk5inout.add(res[i][0])
        i = 0
        countnohistory=0
        counthistory=0
        start = default_timer()
        print "Started"
        timesaved = 0
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            ele_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery13(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value, pkinout,
                                           pk2inout, pk3inout, pk4inout, pk5inout, code_changed_1, code_changed_2) == False:
                self.data[index][1] = 0
            else:
                self.data[index][1] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        print "Query 13 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        return [default_timer() - start, float(counthistory)/len(self.support_set), float(countnohistory)/len(self.support_set), timesaved, endq - beginq, endq - beginq]

    def willOutputChangeQuery13(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value, pkinout,
                                           pk2inout, pk3inout, pk4inout, pk5inout, code_changed_1, code_changed_2):
        if ('lineorder_view' not in ele_1[0]):
            return False
        if ele_2 == None:
            if code_changed_1 in pkinout:
                if 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0] and (not str(ele_1_value).startswith('199402')): #static check for week num TBD
                    return True
                if 'SET lo_quantity' in ele_1[0] and (int(ele_1_value) > 35 or int(ele_1_value) < 26):
                    return True
                if 'SET lo_discount' in ele_1[0] and (int(ele_1_value) > 7 or int(ele_1_value) < 5):
                    return True
            else:
                if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value).startswith('199402') and (code_changed_1 in pk2inout or code_changed_1 in pk3inout):
                    return True
                if 'SET lo_discount' in ele_1[0] and int(ele_1_value) < 7 and int(ele_1_value) > 5 and code_changed_1 in pk4inout:
                    return True
                if 'SET lo_quantity' in ele_1[0] and int(ele_1_value) <=35 and int(ele_1_value) >=26 and code_changed_1 in pk5inout:
                    return True
        else:
            if code_changed_1 not in pkinout and code_changed_2 not in pkinout:
                if 'SET lo_discount' in ele_1[0]:
                    if code_changed_1 in pk4inout:
                        if code_changed_2 not in pk4inout:
                            if ele_1_value < 7 and ele_1_value > 5:
                                return True
                    else:
                        if code_changed_2 in pk4inout:
                            if ele_2_value < 7 and ele_2_value > 5:
                                return True
                if 'SET lo_quantity' in ele_1[0]:
                    if code_changed_1 in pk5inout:
                        if code_changed_2 not in pk5inout:
                            if ele_1_value <= 35 and ele_1_value >= 26:
                                return True
                    else:
                        if code_changed_2 in pk5inout:
                            if ele_1_value <= 35 and ele_1_value >= 26:
                                return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if code_changed_1 in pk2inout or code_changed_1 in pk3inout:
                        if code_changed_2 not in pk2inout and code_changed_2 not in pk3inout:
                            if str(ele_1_value).startswith('199402'):
                                return True
                    else:
                        if code_changed_2 in pk2inout or code_changed_2 in pk3inout:
                            if str(ele_2_value).startswith('199402'):
                                return True
            else:
                if 'SET lo_discount' in ele_1[0] or 'SET lo_extendedprice' in ele_1[0]:
                    return True
                if 'SET lo_orderdate' in ele_1[0]:
                    if (not str(ele_1_value).startswith('199402') or not str(ele_2_value).startswith('199402')):
                        return True
                    else:
                        if code_changed_1 in pk2inout or code_changed_1 in pk3inout:
                            if code_changed_2 not in pk2inout and code_changed_2 not in pk3inout:
                                if str(ele_1_value).startswith('199402'):
                                    return True
                        else:
                            if code_changed_2 in pk2inout or code_changed_2 in pk3inout:
                                if str(ele_2_value).startswith('199402'):
                                    return True
                if 'SET lo_quantity' in ele_1[0]:
                    if ((ele_1_value > 35 and ele_1_value < 26) or (ele_1_value > 35 and ele_1_value < 26)):
                        return True
                    else:
                        if code_changed_1 in pk2inout:
                            if code_changed_2 not in pk2inout:
                                if ele_1_value <= 35 and ele_1_value >= 26:
                                    return True
                        else:
                            if code_changed_2 in pk2inout:
                                if ele_2_value <= 35 and ele_2_value >= 26:
                                    return True
        return False

    def Query2(self):
        query1 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from (select * from lineorder limit 500000) as lineorder , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_category = \'MFGR#12\' and s_region = \'AMERICA\''
        query2 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_category != \'MFGR#12\' and s_region = \'AMERICA\''
        query3 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_category = \'MFGR#12\' and s_region != \'AMERICA\''
        query4 = 'select p_partkey, p_category, p_brand1 from part;'
        query5 = 'select s_suppkey from supplier where s_region = \'AMERICA\';'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        dictlopkyear = {}
        dictlopkbrand = {}
        dictpkbrand = {}
        sinout = Set([])
        pinout = Set([])
        count = 0
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][1])
            pinout.add(res[i][2])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkbrand[res[i][0]] = res[i][4]
            dictpkbrand[res[i][2]] = res[i][4]
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk2inout = Set([])
        sin2out = Set([])
        pin2out = Set([])
        for i in range(0, len(res)):
            lopk2inout.add(res[i][0])
            sin2out.add(res[i][1])
            pin2out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk3inout = Set([])
        sin3out = Set([])
        pin3out = Set([])
        for i in range(0, len(res)):
            lopk3inout.add(res[i][0])
            sin3out.add(res[i][1])
            pin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        dictpartcategory = {}
        dictpartbrand = {}
        for i in range(0, len(res)):
            dictpartcategory[res[i][0]] = res[i][1]
            dictpartbrand[res[i][0]] = res[i][1]
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        suppregion = Set([])
        for i in range(0, len(res)):
            suppregion.add(res[i][0])
        i = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery2(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                                            lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand,
                                           code_changed_1, code_changed_2, dictpartcategory, dictpartbrand, suppregion) == False:
                self.data[index][2] = 0
            else:
                self.data[index][2] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query6 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from lineorder_view , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_category = \'MFGR#12\' and s_region = \'AMERICA\';'
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 2 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        query7 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        print countrows
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery2(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                               lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                               lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand,code_changed_1,
                               code_changed_2, dictpartcategory, dictpartbrand, suppregion):
        if ('customer_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if ('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
                    if 'SET p_category' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in pin2out and 'SET p_category' in ele_1[0] and 'MFGR#12' in ele_1_value:
                        return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 in sinout:
                    if 'SET s_region' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_region' in ele_1[0] and 'AMERICA' in ele_1_value:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0]:
                        try:
                            if not str(ele_1_value).startswith(str(dictlopkyear[code_changed_1])):
                                return True
                        except:
                            None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and int(ele_1_value) not in suppregion:
                        return True
                    if 'SET lo_partkey' in ele_1[0]:
                        try:
                            if 'MFGR#12' not in dictpartcategory[ele_1_value]:
                                return True
                            else:
                                if dictpartbrand[ele_1_value] != dictpartbrand[ele_undo_1_value]:
                                    return True
                        except:
                            None
                else:
                    if 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                        # this can be made static check
                        # if ele_1_value in suppregion:
                        #     return True
                        # if 'SET lo_partkey' in ele_1[0]:
                        #     if 'MFGR#12' in dictpartcategory[ele_1_value]:
                        #     return True

        else:
            if ('part_view' in ele_1[0]):
                if code_changed_1 not in pinout and code_changed_2 not in pinout:
                    if 'SET p_category' in ele_1[0]:
                        if code_changed_1 in pin2out:
                            if code_changed_2 not in pin2out:
                                try:
                                    if 'MFGR#12' in dictpartcategory[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if 'MFGR#12' in dictpartcategory[ele_2_value]:
                                    return True
                            except:
                                None
                else:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
                    if 'SET p_category' in ele_1[0]:
                        if 'MFGR#12' not in ele_1_value and 'MFGR#12' not in ele_2_value:
                            return True
                        else:
                            if code_changed_1 in pinout:
                                if code_changed_2 not in pinout:
                                    try:
                                        if 'MFGR#12' not in ele_1_value or \
                                                ('MFGR#12' in ele_1_value and dictpkbrand[code_changed_1] != dictpartbrand[code_changed_2]):
                                            return True
                                    except:
                                        None
                            else:
                                if code_changed_2 in pinout:
                                    try:
                                        if 'MFGR#12' not in ele_2_value or \
                                                ('MFGR#12' in ele_2_value and dictpkbrand[code_changed_1] != dictpartbrand[code_changed_2]):
                                            return True
                                    except:
                                        None
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'AMERICA' in ele_2_value:
                                    return True
                else:
                    if 'SET s_region' in ele_1[0]:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        #this can also be made static checks
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_2))
                        dbutils.DBUtils.cursor.execute(ele_2[0])
                else:
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                                         or dictpkbrand[code_changed_1] != dictpkbrand[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                if ele_1_value not in suppregion:
                                    return True
                        else:
                            if code_changed_2 in lopkinout:
                                if ele_2_value not in suppregion:
                                    return True
                    if 'SET lo_partkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictpartbrand[ele_1_value] != dictpartbrand[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if 'MFGR#12' not in dictpartcategory[ele_1_value] or \
                                            ('MFGR#12' in dictpartcategory[ele_1_value] and dictpartbrand[ele_2_value]\
                                            != dictpartbrand[ele_1_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'MFGR#12' not in dictpartcategory[ele_2_value] or \
                                            ('MFGR#12' in dictpartcategory[ele_2_value] and dictpartbrand[ele_1_value]\
                                                != dictpartbrand[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                        return True
                                except:
                                    None
        return False

    def Query21(self):
        query1 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from (select * from lineorder limit 500000) as lineorder , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 between \'MFGR#2220\' and \'MFGR#2229\' and s_region = \'ASIA\''
        query2 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 not between \'MFGR#2220\' and \'MFGR#2229\' and s_region = \'ASIA\''
        query3 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 between \'MFGR#2220\' and \'MFGR#2229\' and s_region != \'ASIA\''
        query4 = 'select p_partkey, p_category, p_brand1 from part;'
        query5 = 'select s_suppkey from supplier where s_region = \'AMERICA\';'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        dictlopkyear = {}
        dictlopkbrand = {}
        dictpkbrand = {}
        sinout = Set([])
        pinout = Set([])
        count = 0
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][1])
            pinout.add(res[i][2])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkbrand[res[i][0]] = res[i][4]
            dictpkbrand[res[i][2]] = res[i][4]
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk2inout = Set([])
        sin2out = Set([])
        pin2out = Set([])
        for i in range(0, len(res)):
            lopk2inout.add(res[i][0])
            sin2out.add(res[i][1])
            pin2out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk3inout = Set([])
        sin3out = Set([])
        pin3out = Set([])
        for i in range(0, len(res)):
            lopk3inout.add(res[i][0])
            sin3out.add(res[i][1])
            pin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        dictpartcategory = {}
        dictpartbrand = {}
        for i in range(0, len(res)):
            dictpartcategory[res[i][0]] = res[i][1]
            dictpartbrand[res[i][0]] = res[i][1]
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        suppregion = Set([])
        for i in range(0, len(res)):
            suppregion.add(res[i][0])
        i = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery21(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                                            lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand, dictpartcategory, dictpartbrand,
                                           code_changed_1, code_changed_2, suppregion) == False:
                self.data[index][2] = 0
            else:
                self.data[index][2] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query6 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from (select * from lineorder limit 500000) as lineorder_view , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 between \'MFGR#2221\' and \'MFGR#2228\' and s_region = \'ASIA\''
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 21 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        query7 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, beginq - endq,(beginadhoc - endadhoc)*countrows]

    def willOutputChangeQuery21(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                                            lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand, dictpartcategory, dictpartbrand,
                                           code_changed_1, code_changed_2, suppregion):

        if ('customer_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if ('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in pin2out and 'MFGR#222' in ele_1_value:
                        return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 in sinout:
                    if 'SET s_region' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_region' in ele_1[0] and 'ASIA' in ele_1_value:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0]:
                        try:
                            if not str(ele_1_value).startswith(str(dictlopkyear[code_changed_1])):
                                return True
                        except:
                            None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and int(ele_1_value) not in suppregion:
                        return True
                    if 'SET lo_partkey' in ele_1[0]:
                        try:
                            if dictpartbrand[ele_1_value] != dictpartbrand[ele_undo_1_value]:
                                return True
                        except:
                            None
                else:
                    if 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                        # this can be made static check
                        # if ele_1_value in suppregion:
                        #     return True
                        # if 'SET lo_partkey' in ele_1[0]:
                        #     if 'MFGR#12' in dictpartcategory[ele_1_value]:
                        #     return True

        else:
            if ('part_view' in ele_1[0]):
                if code_changed_1 not in pinout and code_changed_2 not in pinout:
                    if 'SET p_brand1' in ele_1[0]:
                        if code_changed_1 in pin2out:
                            if code_changed_2 not in pin2out:
                                try:
                                    if 'MFGR#222' in dictpartcategory[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if 'MFGR#12' in dictpartcategory[ele_2_value]:
                                    return True
                            except:
                                None
                else:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'ASIA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'ASIA' in ele_2_value:
                                    return True
                else:
                    if 'SET s_region' in ele_1[0]:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        #this can also be made static checks
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                                             or dictpkbrand[code_changed_1] != dictpkbrand[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                if ele_1_value not in suppregion:
                                    return True
                        else:
                            if code_changed_2 in lopkinout:
                                if ele_2_value not in suppregion:
                                    return True
                    if 'SET lo_partkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictpartbrand[ele_1_value] != dictpartbrand[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if dictpartbrand[ele_2_value] != dictpartbrand[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictpartbrand[ele_1_value] != dictpartbrand[ele_2_value]:
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                        return True
                                except:
                                    None
        return False


    def Query22(self):
        query1 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from (select * from lineorder limit 500000) as lineorder , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 = \'MFGR#2221\' and s_region = \'EUROPE\''
        query2 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 != \'MFGR#2221\' and s_region = \'EUROPE\''
        query3 = 'select lo_pk, s_suppkey, p_partkey  from (select * from lineorder limit 500000) as lineorder  , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 = \'MFGR#2221\' and s_region != \'EUROPE\''
        query4 = 'select p_partkey, p_category, p_brand1 from part;'
        query5 = 'select s_suppkey from supplier where s_region = \'EUROPE\';'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        dictlopkyear = {}
        dictlopkbrand = {}
        dictpkbrand = {}
        sinout = Set([])
        pinout = Set([])
        count = 0
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][1])
            pinout.add(res[i][2])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkbrand[res[i][0]] = res[i][4]
            dictpkbrand[res[i][2]] = res[i][4]
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk2inout = Set([])
        sin2out = Set([])
        pin2out = Set([])
        for i in range(0, len(res)):
            lopk2inout.add(res[i][0])
            sin2out.add(res[i][1])
            pin2out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        lopk3inout = Set([])
        sin3out = Set([])
        pin3out = Set([])
        for i in range(0, len(res)):
            lopk3inout.add(res[i][0])
            sin3out.add(res[i][1])
            pin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        dictpartcategory = {}
        dictpartbrand = {}
        for i in range(0, len(res)):
            dictpartcategory[res[i][0]] = res[i][1]
            dictpartbrand[res[i][0]] = res[i][1]
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        suppregion = Set([])
        for i in range(0, len(res)):
            suppregion.add(res[i][0])
        i = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery22(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                                            lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand,
                                           code_changed_1, code_changed_2, dictpartcategory, dictpartbrand, suppregion) == False:
                self.data[index][2] = 0
            else:
                self.data[index][2] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)*10
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query6 = 'select lo_pk, s_suppkey, p_partkey, d_year, p_brand1  from lineorder_view , dwdate , part , supplier  where lo_orderdate = d_datekey and lo_partkey = p_partkey and lo_suppkey = s_suppkey and p_brand1 = \'MFGR#2221\' and s_region = \'EUROPE\';'
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 22 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query7 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (endq - beginq), (endadhoc - beginadhoc)*countrows]

    def willOutputChangeQuery22(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, pinout, dictlopkyear, dictlopkbrand,
                                            lopk2inout, sin2out, pin2out, lopk3inout, sin3out, pin3out,dictpkbrand,
                                           code_changed_1, code_changed_2, dictpartcategory, dictpartbrand, suppregion):

        if ('customer_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if ('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in pin2out and 'SET p_brand1' in ele_1[0] and 'MFGR#2221' in ele_1_value:
                        return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 in sinout:
                    if 'SET s_region' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_region' in ele_1[0] and 'EUROPE' in ele_1_value:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0]:
                        try:
                            if not str(ele_1_value).startswith(str(dictlopkyear[code_changed_1])):
                                return True
                        except:
                            None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and int(ele_1_value) not in suppregion:
                        return True
                    if 'SET lo_partkey' in ele_1[0]:
                        try:
                            if 'MFGR#2221' not in dictpartbrand[ele_1_value]:
                                return True
                            else:
                                if dictpartbrand[ele_1_value] != dictpartbrand[ele_undo_1_value]:
                                    return True
                        except:
                            None
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                        # this can be made static check
                        # if ele_1_value in suppregion:
                        #     return True
                        # if 'SET lo_partkey' in ele_1[0]:
                        #     if 'MFGR#12' in dictpartcategory[ele_1_value]:
                        #     return True

        else:
            if ('part_view' in ele_1[0]):
                if code_changed_1 not in pinout and code_changed_2 not in pinout:
                    if 'SET p_brand1' in ele_1[0]:
                        if code_changed_1 in pin2out:
                            if code_changed_2 not in pin2out:
                                try:
                                    if 'MFGR#2221' in dictpartcategory[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if 'MFGR#12' in dictpartcategory[ele_2_value]:
                                    return True
                            except:
                                None
                else:
                    if 'SET p_brand1' in ele_1[0]:
                        return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'EUROPE' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'EUROPE' in ele_2_value:
                                    return True
                else:
                    if 'SET s_region' in ele_1[0]:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        #this can also be made static checks
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                                         or dictpkbrand[code_changed_1] != dictpkbrand[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                if ele_1_value not in suppregion:
                                    return True
                        else:
                            if code_changed_2 in lopkinout:
                                if ele_2_value not in suppregion:
                                    return True
                    if 'SET lo_partkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictpartbrand[ele_1_value] != dictpartbrand[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if 'MFGR#12' in dictpartcategory[ele_1_value] and dictpartbrand[ele_2_value]\
                                            != dictpartbrand[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if 'MFGR#12' in dictpartcategory[ele_2_value] and dictpartbrand[ele_1_value]\
                                            != dictpartbrand[ele_2_value]:
                                    return True
                            except:
                                None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None
        return False


    def Query3(self):
        query1 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_nation, s_nation from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_region = \'ASIA\' and s_region = \'ASIA\' and d_year >= 1992 and d_year <= 1997  ';
        query2 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_nation, s_nation from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_region != \'ASIA\' and s_region = \'ASIA\' and d_year >= 1992 and d_year <= 1997  ;'
        query3 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_nation, s_nation from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_region = \'ASIA\' and s_region != \'ASIA\' and d_year >= 1992 and d_year <= 1997  ;'
        query4 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_nation, s_nation from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_region = \'ASIA\' and s_region = \'ASIA\' and (d_year < 1992 or d_year > 1997)  ;'
        query5 = 'select s_suppkey, s_nation from supplier where s_region = \'ASIA\'';
        query6 = 'select c_custkey, c_nation from customer where c_region = \'ASIA\'';
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        dictlopkyear = {}
        dictlopkcnation = {}
        dictlopksnation = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkcnation[res[i][0]] = res[i][4]
            dictlopksnation[res[i][0]] = res[i][5]
        cin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        sin3out = Set([])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        lopkyear = Set([])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            lopkyear.add(res[i][0])
        start = default_timer()
        suppkeyasia = Set([])
        dictsuppsnation = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            suppkeyasia.add(res[i][0])
            dictsuppsnation[res[i][0]] = res[i][1]
        custkeyasia = Set([])
        dictcustcnation = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            custkeyasia.add(res[i][0])
            dictcustcnation[res[i][0]] = res[i][1]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            ele_undo_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery3(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeyasia, custkeyasia, dictcustcnation, dictsuppsnation,
                                           dictlopkyear, dictlopkcnation, dictlopksnation) == False:
                self.data[index][3] = 0
            else:
                self.data[index][3] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        query7 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_nation, s_nation from customer , lineorder_view, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_region = \'ASIA\' and s_region = \'ASIA\' and d_year >= 1992 and d_year <= 1997  ;'
        beginadhoc = default_timer()
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 3 : ",countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query8 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query8)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery3(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeyasia, custkeyasia, dictcnation, dictsuppsnation,
                                           dictlopkyear, dictlopkcnation, dictlopksnation):
        if ('part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_nation' in ele_1[0] or 'SET c_region' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in cin2out and 'SET c_region' in ele_1[0] and 'ASIA' in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_nation' in ele_1[0] or 'SET s_region' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_region' in ele_1[0] and 'ASIA' in ele_1_value:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value)[:4] != str(ele_undo_1_value)[:4]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if int(ele_1_value) not in suppkeyasia:
                            return True
                        else:
                            try:
                                if dictsuppsnation[int(ele_1_value)] != dictsuppsnation[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                    if 'SET lo_custkey' in ele_1[0]:
                        if int(ele_1_value) not in custkeyasia:
                            return True
                        else:
                            if dictcnation[int(ele_1_value)] != dictcnation[int(ele_undo_1_value)]:
                                return True
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_region' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if 'ASIA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if 'ASIA' in ele_2_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET c_nation' in ele_1[0]:
                                return True
                        else:
                            if 'SET c_nation' in ele_1[0] or 'SET c_region' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_nation' in ele_1[0] or 'SET c_region' in ele_1[0]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'ASIA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'ASIA' in ele_2_value:
                                    return True
                else:
                    if code_changed_1 in sinout:
                        if code_changed_2 in sinout:
                            if 'SET s_nation' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_nation' in ele_1[0] or 'SET s_region' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in sinout:
                            if 'SET s_nation' in ele_1[0] or 'SET s_region' in ele_1[0]:
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                    #return False
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictcnation[ele_1_value] != dictcnation[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in custkeyasia or \
                                            (ele_1_value in custkeyasia and dictcnation[ele_1_value] != dictcnation[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in custkeyasia or \
                                            (ele_2_value in custkeyasia and dictcnation[ele_2_value] != dictcnation[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                        or dictlopkcnation[code_changed_1] != dictlopkcnation[code_changed_2]
                                        or dictlopksnation[code_changed_1] != dictlopksnation[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppsnation[ele_1_value] != dictsuppsnation[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in suppkeyasia or \
                                            (ele_1_value in suppkeyasia and dictsuppsnation[ele_1_value] != dictsuppsnation[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in suppkeyasia or \
                                            (ele_2_value in suppkeyasia and dictsuppsnation[ele_2_value] != dictsuppsnation[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None
        return False

    def Query31(self):
        query1 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation = \'UNITED STATES\' and s_nation = \'UNITED STATES\' and d_year >= 1992 and d_year <= 1997  ;';
        query2 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation != \'UNITED STATES\' and s_nation = \'UNITED STATES\' and d_year >= 1992 and d_year <= 1997 ;'
        query3 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation = \'UNITED STATES\' and s_nation != \'UNITED STATES\' and d_year >= 1992 and d_year <= 1997 ;'
        query4 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation = \'UNITED STATES\' and s_nation = \'UNITED STATES\' and (d_year < 1992 or d_year > 1997)  ;'
        query5 = 'select s_suppkey, s_city from supplier where s_nation = \'UNITED STATES\'';
        query6 = 'select c_custkey, c_city from customer where c_nation = \'UNITED STATES\'';
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        dictlopkyear = {}
        dictlopkccity = {}
        dictlopkscity = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkccity[res[i][0]] = res[i][4]
            dictlopkscity[res[i][0]] = res[i][5]
        cin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        sin3out = Set([])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        lopkyear = Set([])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            lopkyear.add(res[i][0])
        start = default_timer()
        suppkeyasia = Set([])
        dictsuppscity = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            suppkeyasia.add(res[i][0])
            dictsuppscity[res[i][0]] = res[i][1]
        custkeyasia = Set([])
        dictcustccity = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            custkeyasia.add(res[i][0])
            dictcustccity[res[i][0]] = res[i][1]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            ele_undo_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            current = default_timer()
            if self.willOutputChangeQuery31(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeyasia, custkeyasia, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity) == False:
                self.data[index][3] = 0
            else:
                self.data[index][3] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        query7 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder_view, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation = \'UNITED STATES\' and s_nation = \'UNITED STATES\' and d_year >= 1992 and d_year <= 1997 ;'
        beginadhoc = default_timer()
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 31 : ", countnohistory, counthistory
        print "time : ", default_timer() - start
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query8 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query8)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery31(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeyasia, custkeyasia, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity):
        if ('part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_nation' in ele_1[0] or 'SET c_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in cin2out and 'SET c_nation' in ele_1[0] and 'UNITED STATES' in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_nation' in ele_1[0] or 'SET s_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_nation' in ele_1[0] and 'UNITED STATES' in ele_1_value:
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value).startswith('1998'):
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if int(ele_1_value) not in suppkeyasia:
                            return True
                        else:
                            try:
                                if dictsuppscity[int(ele_1_value)] != dictsuppscity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                    if 'SET lo_custkey' in ele_1[0]:
                        if int(ele_1_value) not in custkeyasia:
                            return True
                        else:
                            try:
                                if dictcustccity[int(ele_1_value)] != dictcustccity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_nation' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if 'UNITED STATES' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if 'UNITED STATES' in ele_2_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET c_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET c_nation' in ele_1[0] or 'SET c_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_nation' in ele_1[0] or 'SET c_city' in ele_1[0]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_nation' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'UNITED STATES' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'UNITED STATES' in ele_2_value:
                                    return True
                else:
                    if code_changed_1 in sinout:
                        if code_changed_2 in sinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_nation' in ele_1[0] or 'SET s_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in sinout:
                            if 'SET s_nation' in ele_1[0] or 'SET s_city' in ele_1[0]:
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                    #return False
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictcustccity[ele_1_value] != dictcustccity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in custkeyasia or \
                                            (ele_1_value in custkeyasia and dictcustccity[ele_1_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in custkeyasia or \
                                            (ele_2_value in custkeyasia and dictcustccity[ele_2_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                        or dictlopkccity[code_changed_1] != dictlopkccity[code_changed_2]
                                        or dictlopkscity[code_changed_1] != dictlopkscity[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in suppkeyasia or \
                                            (ele_1_value in suppkeyasia and dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in suppkeyasia or \
                                            (ele_2_value in suppkeyasia and dictsuppscity[ele_2_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None

        return False


    def Query32(self):

        query1 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_year >= 1992 and d_year <= 1997  ';
        query2 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city!=\'UNITED KI1\' and c_city!=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_year >= 1992 and d_year <= 1997  ;'
        query3 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city!=\'UNITED KI1\' and s_city!=\'UNITED KI5\') and d_year >= 1992 and d_year <= 1997  ;'
        query4 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and (d_year < 1992 or d_year > 1997)  ;'
        query5 = 'select s_suppkey, s_city from supplier where (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\')';
        query6 = 'select c_custkey, c_city from customer where (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\')';
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        dictlopkyear = {}
        dictlopkccity = {}
        dictlopkscity = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkccity[res[i][0]] = res[i][4]
            dictlopkscity[res[i][0]] = res[i][5]
        cin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        sin3out = Set([])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        lopkyear = Set([])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            lopkyear.add(res[i][0])
        start = default_timer()
        suppkeycity = Set([])
        dictsuppscity = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            suppkeycity.add(res[i][0])
            dictsuppscity[res[i][0]] = res[i][1]
        custkeycity = Set([])
        dictcustccity = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            custkeycity.add(res[i][0])
            dictcustccity[res[i][0]] = res[i][1]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            ele_undo_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery32(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeycity, custkeycity, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity) == False:
                self.data[index][3] = 0
            else:
                self.data[index][3] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query7 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder_view, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_year >= 1992 and d_year <= 1997  ;'
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 32 : ", countnohistory, counthistory
        print "time : ", default_timer() - start
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query8 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query8)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery32(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeycity, custkeycity, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity):
        if ('part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in cin2out and 'SET c_city' in ele_1[0] and ('UNITED KI1' in ele_1_value\
                            or 'UNITED KI5' in ele_1_value):
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_city' in ele_1[0] and ('UNITED KI1' in ele_1_value\
                            or 'UNITED KI5' in ele_1_value):
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and str(ele_1_value).startswith('1998'):
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if int(ele_1_value) not in suppkeycity:
                            return True
                        else:
                            try:
                                if dictsuppscity[int(ele_1_value)] != dictsuppscity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                    if 'SET lo_custkey' in ele_1[0]:
                        if int(ele_1_value) not in custkeycity:
                            return True
                        else:
                            try:
                                if dictcustccity[int(ele_1_value)] != dictcustccity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_city' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET c_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET c_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_city' in ele_1[0]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_city' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                else:
                    if code_changed_1 in sinout:
                        if code_changed_2 in sinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in sinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictcustccity[ele_1_value] != dictcustccity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in custkeycity or \
                                            (ele_1_value in custkeycity and dictcustccity[ele_1_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in custkeycity or \
                                            (ele_2_value in custkeycity and dictcustccity[ele_2_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                        or dictlopkccity[code_changed_1] != dictlopkccity[code_changed_2]
                                        or dictlopkscity[code_changed_1] != dictlopkscity[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in suppkeycity or \
                                            (ele_1_value in suppkeycity and dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in suppkeycity or \
                                            (ele_2_value in suppkeycity and dictsuppscity[ele_2_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None

        return False


    def Query33(self):

        query1 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_yearmonth = \'Dec1997\'  ';
        query2 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city!=\'UNITED KI1\' and c_city!=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_yearmonth = \'Dec1997\'  ;'
        query3 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city!=\'UNITED KI1\' and s_city!=\'UNITED KI5\') and d_yearmonth = \'Dec1997\'  ;'
        query4 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_yearmonth != \'Dec1997\'  ;'
        query5 = 'select s_suppkey, s_city from supplier where (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\')';
        query6 = 'select c_custkey, c_city from customer where (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\')';
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        dictlopkyear = {}
        dictlopkccity = {}
        dictlopkscity = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            dictlopkyear[res[i][0]] = res[i][3]
            dictlopkccity[res[i][0]] = res[i][4]
            dictlopkscity[res[i][0]] = res[i][5]
        cin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        sin3out = Set([])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        lopkyear = Set([])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            lopkyear.add(res[i][0])
        start = default_timer()
        suppkeycity = Set([])
        dictsuppscity = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            suppkeycity.add(res[i][0])
            dictsuppscity[res[i][0]] = res[i][1]
        custkeycity = Set([])
        dictcustccity = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            custkeycity.add(res[i][0])
            dictcustccity[res[i][0]] = res[i][1]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            ele_undo_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_value[i + 1]
                ele_undo_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery33(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeycity, custkeycity, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity) == False:
                self.data[index][3] = 0
            else:
                self.data[index][3] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query7 = 'select lo_pk, c_custkey, s_suppkey, d_year, c_city, s_city from customer , lineorder_view, supplier , dwdate  where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and (s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_yearmonth = \'Dec1997\' ;'
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 33 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query8 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query8)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery33(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_undo_2_value, ele_2_value,
                                           lopkinout, sinout, cinout, cin2out, sin3out, lopkyear, code_changed_1,
                                           code_changed_2, suppkeycity, custkeycity, dictcustccity, dictsuppscity,
                                           dictlopkyear, dictlopkccity, dictlopkscity):
        if ('part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in cin2out and 'SET c_city' in ele_1[0] and ('UNITED KI1' in ele_1_value\
                            or 'UNITED KI5' in ele_1_value):
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_city' in ele_1[0]:
                        return True
                else:
                    if code_changed_1 in sin3out and 'SET s_city' in ele_1[0] and ('UNITED KI1' in ele_1_value\
                            or 'UNITED KI5' in ele_1_value):
                        return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and not str(ele_1_value).startswith('199712'):
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if int(ele_1_value) not in suppkeycity:
                            return True
                        else:
                            try:
                                if dictsuppscity[int(ele_1_value)] != dictsuppscity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                    if 'SET lo_custkey' in ele_1[0]:
                        if int(ele_1_value) not in custkeycity:
                            return True
                        else:
                            try:
                                if dictcustccity[int(ele_1_value)] != dictcustccity[int(ele_undo_1_value)]:
                                    return True
                            except:
                                None
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_city' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET c_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET c_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_city' in ele_1[0]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_city' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if ('UNITED KI1' in ele_1_value or 'UNITED KI5' in ele_1_value):
                                    return True
                else:
                    if code_changed_1 in sinout:
                        if code_changed_2 in sinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_city' in ele_1[0]:
                                return True
                    else:
                        if code_changed_2 in sinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictcustccity[ele_1_value] != dictcustccity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in custkeycity or \
                                            (ele_1_value in custkeycity and dictcustccity[ele_1_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in custkeycity or \
                                            (ele_2_value in custkeycity and dictcustccity[ele_2_value] != dictcustccity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if (dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]
                                        or dictlopkccity[code_changed_1] != dictlopkccity[code_changed_2]
                                        or dictlopkscity[code_changed_1] != dictlopkscity[code_changed_2]):
                                        return True
                                except:
                                    None
                            else:
                                return True
                        else:
                            if code_changed_2 in lopkinout:
                                return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if ele_1_value not in suppkeycity or \
                                            (ele_1_value in suppkeycity and dictsuppscity[ele_1_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if ele_2_value not in suppkeycity or \
                                            (ele_2_value in suppkeycity and dictsuppscity[ele_2_value] != dictsuppscity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if not str(ele_1_value)[:6].startswith('199712'):
                                        return True
                                except:
                                    None
                        else:
                            try:
                                if not str(ele_1_value)[:6].startswith('199712'):
                                    return True
                            except:
                                None

        return False



    def Query4(self):
        query1 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\');'
        query2 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region != \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\');'
        query3 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region != \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\');'
        query4 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr != \'MFGR#1\' and p_mfgr != \'MFGR#2\');'
        query5 = 'select c_custkey, c_nation, c_region from customer'
        query6 = 'select s_suppkey, s_nation, s_region from supplier'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        pinout = Set([])
        dictlopkyear = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            pinout.add(res[i][3])
            dictlopkyear[res[i][0]] = res[i][5]
        cin2out = Set([])
        sin3out = Set([])
        pin4out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            pin4out.add(res[i][3])
        dictcustnation = {}
        dictcustregion = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictcustnation[res[i][0]] = res[i][1]
            dictcustregion[res[i][0]] = res[i][2]
        dictsuppnation = {}
        dictsuppregion = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictsuppnation[res[i][0]] = res[i][1]
            dictsuppregion[res[i][0]] = res[i][2]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        print "Started"
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery4(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppregion, code_changed_1, code_changed_2) == False:
                self.data[index][4] = 0
            else:
                self.data[index][4] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)*70
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query7 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, lineorder_view where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\');'
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 4 : ", countnohistory, counthistory
        print "time : ", default_timer() - start, timesaved
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query8 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query8)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery4(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppregion, code_changed_1, code_changed_2):
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_region' in ele_1[0] or 'SET c_nation':
                        return True
                else:
                    if 'SET c_region' in ele_1[0] and code_changed_1 in cin2out and 'AMERICA' in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_region' in ele_1[0]:
                        return True
                else:
                    if 'SET s_region' in ele_1[0] and code_changed_1 in sin3out and 'AMERICA' in ele_1_value:
                        return True
            if('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_mfgr' in ele_1[0] and 'MGFR#1' not in ele_1_value and 'MGFR#2' not in ele_1_value:
                        return True
                    else:
                        if 'SET p_mfgr' in ele_1[0] and code_changed_1 in pin4out and \
                                ('MGFR#1' in ele_1_value or 'MGFR#2' in ele_1_value):
                            return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0] or 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and int(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and 'AMERICA' not in dictsuppregion[ele_1_value]:
                        return True
                    if 'SET lo_custkey' in ele_1[0] and (dictcustregion[ele_1_value]!= 'AMERICA' or
                                                             (dictcustregion[ele_1_value] == 'AMERICA' \
                                            and dictcustnation[ele_1_value] != dictcustnation[ele_undo_1_value])):
                        return True
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_region' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET c_nation' in ele_1[0]:
                                return True
                        else:
                            if 'SET c_nation' in ele_1[0] and dictcustnation[code_changed_1] != dictcustnation[code_changed_2]:
                                return True
                            if 'SET c_region' in ele_1[0] and (dictcustregion[code_changed_1] != 'AMERICA'
                             or (dictcustregion[code_changed_1] == 'AMERICA' and dictcustnation[code_changed_1] != dictcustnation[code_changed_2])):
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_nation' in ele_1[0] and dictcustnation[code_changed_2] != dictcustnation[code_changed_1]:
                                return True
                            if 'SET c_region' in ele_1[0] and (dictcustregion[code_changed_2] != 'AMERICA'
                             or (dictcustregion[code_changed_2] == 'AMERICA' and dictcustnation[code_changed_1] != dictcustnation[code_changed_2])):
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in sinout and code_changed_2 not in sinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in sin3out:
                            if code_changed_2 not in sin3out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in sinout:
                        if code_changed_2 not in sinout:
                            if 'SET s_region' in ele_1[0] and 'AMERICA' in ele_1_value:
                                return True
                    else:
                        if code_changed_2 in sinout:
                            if 'SET s_region' in ele_1[0] and 'AMERICA' in ele_2_value:
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictcustnation[ele_1_value] != dictcustnation[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_1_value] or \
                                            ('AMERICA' in dictcustregion[ele_1_value] and \
                                                     dictcustnation[ele_1_value] != dictcustnation[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_2_value] or \
                                            ('AMERICA' in dictcustregion[ele_2_value] and \
                                                     dictcustnation[ele_1_value] != dictcustnation[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if 'AMERICA' not in dictsuppregion[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'AMERICA' not in dictsuppregion[ele_2_value]:
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None
        return False


    def Query41(self):
        query1 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        query2 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region != \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        query3 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region != \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        query4 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr != \'MFGR#1\' and p_mfgr != \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        query5 = 'select c_custkey, c_nation, c_region from customer'
        query6 = 'select s_suppkey, s_nation, s_region from supplier'
        query7 = 'select p_partkey, p_mfgr, p_category from part'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        pinout = Set([])
        dictlopkyear = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            pinout.add(res[i][3])
            dictlopkyear[res[i][0]] = res[i][5]
        cin2out = Set([])
        sin3out = Set([])
        pin4out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            pin4out.add(res[i][3])
        dictcustnation = {}
        dictcustregion = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictcustnation[res[i][0]] = res[i][1]
            dictcustregion[res[i][0]] = res[i][2]
        dictsuppnation = {}
        dictsuppregion = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictsuppnation[res[i][0]] = res[i][1]
            dictsuppregion[res[i][0]] = res[i][2]
        dictpartmfgr = {}
        dictpartcategory = {}
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictpartmfgr[res[i][0]] = res[i][1]
            dictpartcategory[res[i][0]] = res[i][2]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        print "Started"
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery41(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppregion,
                                           dictpartcategory, dictpartmfgr, code_changed_1, code_changed_2) == False:
                self.data[index][4] = 0
            else:
                self.data[index][4] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)*70
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query8 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, lineorder_view where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        dbutils.DBUtils.cursor.execute(query8)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 41 : ", countnohistory, counthistory
        print "time : ", default_timer() - start
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query9 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query9)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows ]

    def willOutputChangeQuery41(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppregion,
                                           dictpartcategory, dictpartmfgr, code_changed_1, code_changed_2):
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_region' in ele_1[0]:
                        return True
                else:
                    if 'SET c_region' in ele_1[0] and code_changed_1 in cin2out and 'AMERICA' in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_region' in ele_1[0]:
                        return True
                    if 'SET s_nation' in ele_1[0]:
                        return True
                else:
                    if 'SET s_region' in ele_1[0] and code_changed_1 in sin3out and 'AMERICA' in ele_1_value:
                        return True
            if('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_category' in ele_1[0]:
                        return True
                    if 'SET p_mfgr' in ele_1[0] and 'MGFR#1' not in ele_1_value and 'MGFR#2' not in ele_1_value:
                        return True
                    else:
                        if 'SET p_mfgr' in ele_1[0] and code_changed_1 in pin4out and \
                                ('MGFR#1' in ele_1_value or 'MGFR#2' in ele_1_value):
                            return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0] or 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and int(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and (dictsuppregion[ele_1_value]!= 'AMERICA' or
                                                             (dictsuppregion[ele_1_value] == 'AMERICA' \
                                            and dictsuppnation[ele_1_value] != dictsuppnation[ele_undo_1_value])):
                        return True
                    if 'SET lo_custkey' in ele_1[0] and 'AMERICA' not in dictcustregion[ele_1_value]:
                        return True
                    if 'SET lo_partkey' in ele_1[0]:
                        if 'MFGR#1' not in dictpartmfgr[ele_1_value] or ('MFGR#1' in dictpartmfgr[ele_1_value] \
                                                                         and dictpartcategory[ele_1_value] !=
                                dictpartcategory[ele_undo_1_value]):
                            return True
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_region' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            None
                        else:
                            if 'SET c_region' in ele_1[0] and 'AMERICA' not in dictcustregion[code_changed_1]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_region' in ele_1[0] and 'AMERICA' not in dictcustregion[code_changed_2]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET s_region' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in sin3out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET s_nation' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_nation' in ele_1[0] and dictsuppnation[code_changed_1] != dictsuppnation[code_changed_2]:
                                return True
                            if 'SET s_region' in ele_1[0] and (dictsuppregion[code_changed_1] != 'AMERICA'
                             or (dictsuppregion[code_changed_1] == 'AMERICA' and dictsuppnation[code_changed_1] != dictsuppnation[code_changed_2])):
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET s_nation' in ele_1[0] and dictsuppnation[code_changed_1] != dictsuppnation[code_changed_2]:
                                return True
                            if 'SET s_region' in ele_1[0] and (dictsuppregion[code_changed_2] != 'AMERICA'
                             or (dictsuppregion[code_changed_2] == 'AMERICA' and dictsuppnation[code_changed_1] != dictsuppnation[code_changed_2])):
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_2_value]:
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppnation[ele_1_value] != dictsuppnation[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if 'AMERICA' not in dictsuppregion[ele_1_value] or \
                                            ('AMERICA' in dictsuppregion[ele_1_value] and \
                                                     dictsuppnation[ele_1_value] != dictsuppnation[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'AMERICA' not in dictsuppregion[ele_2_value] or \
                                            ('AMERICA' in dictsuppregion[ele_2_value] and \
                                                     dictsuppnation[ele_1_value] != dictsuppnation[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None
        return False


    def Query42(self):
        query1 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_nation = \'UNITED STATES\' and p_category = \'MFGR#14\' and (d_year = 1997 or d_year = 1998);'
        query2 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region != \'AMERICA\' and s_nation = \'UNITED STATES\' and p_category = \'MFGR#14\' and (d_year = 1997 or d_year = 1998);'
        query3 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_nation != \'UNITED STATES\' and p_category = \'MFGR#14\' and (d_year = 1997 or d_year = 1998);'
        query4 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation from dwdate, customer, supplier, part, (select * from lineorder limit 100000) as lineorder where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_nation = \'UNITED STATES\' and p_category != \'MFGR#14\' and (d_year = 1997 or d_year = 1998);'
        query5 = 'select c_custkey, c_nation, c_region from customer'
        query6 = 'select s_suppkey, s_nation, s_city from supplier'
        query7 = 'select p_partkey, p_mfgr, p_brand1 from part'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        lopkinout = Set([])
        sinout = Set([])
        cinout = Set([])
        pinout = Set([])
        dictlopkyear = {}
        for i in range(0, len(res)):
            lopkinout.add(res[i][0])
            sinout.add(res[i][2])
            cinout.add(res[i][1])
            pinout.add(res[i][3])
            dictlopkyear[res[i][0]] = res[i][5]
        cin2out = Set([])
        sin3out = Set([])
        pin4out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            cin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sin3out.add(res[i][2])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            pin4out.add(res[i][3])
        dictcustnation = {}
        dictcustregion = {}
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictcustnation[res[i][0]] = res[i][1]
            dictcustregion[res[i][0]] = res[i][2]
        dictsuppnation = {}
        dictsuppcity = {}
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictsuppnation[res[i][0]] = res[i][1]
            dictsuppcity[res[i][0]] = res[i][2]
        dictpartmfgr = {}
        dictpartbrand = {}
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            dictpartmfgr[res[i][0]] = res[i][1]
            dictpartbrand[res[i][0]] = res[i][2]
        i = 0
        count = 0
        countnohistory = 0
        counthistory = 0
        timesaved = 0
        print "Started"
        start = default_timer()
        while (i < len(self.support_set)):
            current = default_timer()
            ele_2 = None
            ele_undo_2 = None
            ele_2_value = None
            code_changed_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                ele_2_value = self.support_set_undo_value[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if self.willOutputChangeQuery42(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppcity,
                                           dictpartbrand, dictpartmfgr, code_changed_1, code_changed_2) == False:
                self.data[index][4] = 0
            else:
                self.data[index][4] = 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.append(i)
                else:
                    timesaved += (default_timer() - current)*70
            if i != len(self.support_set) - 1 and self.support_set[i][1] == self.support_set[i + 1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query8 = 'select lo_pk, c_custkey, s_suppkey, p_partkey, c_nation, d_year from dwdate, customer, supplier, part, lineorder_view where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') and (d_year = 1997 or d_year = 1998);'
        dbutils.DBUtils.cursor.execute(query8)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "Query 42 : ", countnohistory, counthistory
        print "time : ", default_timer() - start
        print "qt: ", beginq - endq
        print "adhoc: ", beginadhoc - endadhoc
        query9 = 'select count(*) from lineorder_view;'
        dbutils.DBUtils.cursor.execute(query9)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        self.cleanup()
        return [default_timer() - start, float(counthistory + len(res))/len(self.support_set), float(countnohistory + len(res))/len(self.support_set), timesaved, (beginq - endq)*-1, -1*(beginadhoc - endadhoc)*countrows]

    def willOutputChangeQuery42(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, ele_2_value,
                                           lopkinout, sinout, cinout, pinout, cin2out, sin3out, pin4out
                                           , dictcustnation, dictcustregion, dictlopkyear, dictsuppnation, dictsuppcity,
                                           dictpartbrand, dictpartmfgr, code_changed_1, code_changed_2):
        if ele_2 == None:
            if 'customer_view' in ele_1[0]:
                if code_changed_1 in cinout:
                    if 'SET c_region' in ele_1[0]:
                        return True
                else:
                    if 'SET c_region' in ele_1[0] and code_changed_1 in cin2out and 'AMERICA' in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 'SET s_nation' in ele_1[0]:
                        return True
                    if 'SET s_city' in ele_1[0]:
                        return True
                else:
                    if 'SET s_nation' in ele_1[0] and code_changed_1 in sin3out and 'UNITED STATES' in ele_1_value:
                        return True
            if('part_view' in ele_1[0]):
                if code_changed_1 in pinout:
                    if 'SET p_category' in ele_1[0]:
                        return True
                    if 'SET p_mfgr' in ele_1[0] and 'MGFR#14' not in ele_1_value:
                        return True
                    else:
                        if 'SET p_mfgr' in ele_1[0] and code_changed_1 in pin4out and \
                                ('MGFR#14' in ele_1_value):
                            return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 in lopkinout:
                    if 'SET lo_revenue' in ele_1[0] or 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_orderdate' in ele_1[0] and int(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0] and (dictsuppnation[ele_1_value]!= 'UNITED STATES' or
                                                             (dictsuppnation[ele_1_value] == 'UNITED STATES' \
                                            and dictsuppcity[ele_1_value] != dictsuppcity[ele_undo_1_value])):
                        return True
                    if 'SET lo_custkey' in ele_1[0] and 'AMERICA' not in dictcustregion[ele_1_value]:
                        return True
                    if 'SET p_partkey' in ele_1[0]:
                        if 'MFGR#14' not in dictpartmfgr[ele_1_value] or ('MFGR#1' in dictpartmfgr[ele_1_value] \
                                                                         and dictpartbrand[ele_1_value] !=
                                dictpartbrand[ele_undo_1_value]):
                            return True
                else:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
        else:
            if ('customer_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET c_region' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in cin2out:
                                if 'AMERICA' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            None
                        else:
                            if 'SET c_region' in ele_1[0] and 'AMERICA' not in dictcustregion[code_changed_1]:
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET c_region' in ele_1[0] and 'AMERICA' not in dictcustregion[code_changed_2]:
                                return True
            if ('supplier_view' in ele_1[0]):
                if code_changed_1 not in cinout and code_changed_2 not in cinout:
                    if 'SET s_nation' in ele_1[0]:
                        if code_changed_1 in cin2out:
                            if code_changed_2 not in sin3out:
                                if 'UNITED STATES' in ele_1_value:
                                    return True
                        else:
                            if code_changed_2 in sin3out:
                                if 'UNITED STATES' in ele_1_value:
                                    return True
                else:
                    if code_changed_1 in cinout:
                        if code_changed_2 in cinout:
                            if 'SET s_city' in ele_1[0]:
                                return True
                        else:
                            if 'SET s_city' in ele_1[0] and dictsuppcity[code_changed_1] != dictsuppcity[code_changed_2]:
                                return True
                            if 'SET s_nation' in ele_1[0] and (dictsuppnation[code_changed_1] != 'UNITED STATES'
                             or (dictsuppnation[code_changed_1] == 'UNITED STATES' and dictsuppcity[code_changed_1] != dictsuppcity[code_changed_2])):
                                return True
                    else:
                        if code_changed_2 in cinout:
                            if 'SET s_city' in ele_1[0] and dictsuppcity[code_changed_1] != dictsuppcity[code_changed_2]:
                                return True
                            if 'SET s_nation' in ele_1[0] and (dictsuppnation[code_changed_2] != 'AMERICA'
                             or (dictsuppnation[code_changed_2] == 'AMERICA' and dictsuppcity[code_changed_1] != dictsuppcity[code_changed_2])):
                                return True
            if ('lineorder_view' in ele_1[0]):
                if code_changed_1 not in lopkinout and code_changed_2 not in lopkinout:
                    if 'SET lo_orderdate' in ele_1[0] or 'SET lo_suppkey' in ele_1[0] or 'SET lo_partkey' in ele_1[0] or 'SET lo_custkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineorder_view select * from lineorder where lo_pk = ' + str(
                                    code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
                else:
                    if 'SET lo_custkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_1_value]:
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'AMERICA' not in dictcustregion[ele_2_value]:
                                        return True
                                except:
                                    None
                    if 'SET lo_revenue' in ele_1[0]:
                        return True
                    if 'SET lo_supplycost' in ele_1[0]:
                        return True
                    if 'SET lo_suppkey' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 in lopkinout:
                                try:
                                    if dictsuppcity[ele_1_value] != dictsuppcity[ele_2_value]:
                                        return True
                                except:
                                    None
                            else:
                                try:
                                    if 'UNITED STATES' not in dictsuppnation[ele_1_value] or \
                                            ('UNITED STATES' in dictsuppnation[ele_1_value] and \
                                                     dictsuppcity[ele_1_value] != dictsuppcity[ele_2_value]):
                                        return True
                                except:
                                    None
                        else:
                            if code_changed_2 in lopkinout:
                                try:
                                    if 'UNITED STATES' not in dictsuppnation[ele_1_value] or \
                                            ('UNITED STATES' in dictsuppnation[ele_1_value] and \
                                                     dictsuppcity[ele_1_value] != dictsuppcity[ele_2_value]):
                                        return True
                                except:
                                    None
                    if 'SET lo_orderdate' in ele_1[0]:
                        if code_changed_1 in lopkinout:
                            if code_changed_2 not in lopkinout:
                                try:
                                    if long(str(ele_1_value)[:4]) != dictlopkyear[code_changed_1]:
                                        return True
                                except:
                                    None
                            else:
                                if dictlopkyear[code_changed_1] != dictlopkyear[code_changed_2]:
                                    return True
                        else:
                            try:
                                if long(str(ele_2_value)[:4]) != dictlopkyear[code_changed_2]:
                                    return True
                            except:
                                None
        return False



    def convertToString(self, queries):
        str = ''
        for i in range(0, len(queries)):
            str = str + queries[i][0] + '\n'
        return str

    def calculatepriceandtime(self):
        queries = [
                    'Query1','Query12','Query13','Query2','Query21','Query22','Query3','Query31','Query32','Query33',
                   'Query4','Query41','Query42'
                   ]
        m = globals()['Combiner']()
        for i in range(0, len(queries)):
            output = getattr(m, queries[i])()
            # print queries[i], output
            self.runningcumprice += output[2]*100 #scaling prices does not violate arbitrage!
            self.runningcumsavings += output[1]*100 #scaling prices does not violate arbitrage!
            self.runningssbcumtime += output[0]
            self.runningssbcumtimesavings += (output[0] + output[3])
            self.ssbcumprice.append(self.runningcumprice)
            self.ssbcumpricesavings.append(self.runningcumsavings)
            self.ssbcumtime.append(self.runningssbcumtime)
            self.ssbcumtimesavings.append(self.runningssbcumtimesavings)
            self.with_sampling.append(output[0])
            self.qt.append(output[4])
            self.naive.append(output[4] + output[5])

    def dishistory(self):
        fig, ax = plt.subplots()
        ax.set_ylim([0, 15])
        ax.set_xlim([0, 14])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 15, 5))
        #ax.yaxis.set_ticks(np.arange(0, 15, 1), minor=False)
        ax.xaxis.set_ticks(np.arange(1,14, 1))
        ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
        #ax.grid(which='minor', alpha=0.2)
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
        ax.plot([x for x in range(1,14)], self.ssbcumprice, color='b', marker='x', markersize=2)
        ax.plot([x for x in range(1,14)], self.ssbcumpricesavings, color='r', marker='s', markersize=2)
        plt.ylabel("Price")
        plt.xlabel("Query")
        lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
        plt.savefig('ssbstatichistoryawareprice.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

    def dishistorytime(self):
        fig, ax = plt.subplots()
        ax.set_ylim([0, 40])
        ax.set_xlim([0, 14])
        #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
        ax.yaxis.set_ticks(np.arange(0, 40, 10))
        #ax.yaxis.set_ticks(np.arange(0, 40, 1), minor=False)
        ax.xaxis.set_ticks(np.arange(1,14, 1))
        ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
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

        ax.plot([x for x in range(1,14)], self.ssbcumtimesavings, color='b', marker='x', markersize=2)
        ax.plot([x for x in range(1,14)], self.ssbcumtime, color='r', marker='s', markersize=2)

        plt.ylabel("Time in s")
        plt.xlabel("Query")
        lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
        plt.savefig('ssbstatichistorytime.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

    def disssb(self):
        mpl.rcParams['figure.figsize'] = 4.44, 1.95
        mpl.rcParams['xtick.labelsize'] = 5
        mpl.rcParams['legend.fontsize'] = 7
        plt.yscale('log')
        fig, ax = plt.subplots()
        ax.set_yscale('log')
        ax.set_ylim([0.05,1000])
        ax.set_xlim([0.8, 14])
        width = 0.2
        ax.xaxis.set_ticks([x + width for x in range(1,14)])
        ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
        #ax.grid(which='minor', alpha=0.2)
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

        ax.bar([x - 0.5*width for x in range(1,14)], [abs(number) for number in self.naive], width, color='blueviolet', linewidth=0.5, bottom = 0)
        ax.bar([x + 0.5*width for x in range(1,14)], [abs(number) for number in self.with_sampling], width, color='dodgerblue', linewidth=0.5, bottom = 0)
        ax.bar([x + 1.5*width for x in range(1,14)], [abs(number) for number in self.qt], width, color='darkorange', linewidth=0.5, bottom = 0)
        plt.ylabel("Time in s")
        plt.xlabel("Query")
        lgd = plt.legend(['no batching','with batching', 'query execution time'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
        plt.savefig('barchartssbtime.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')




if __name__ == "__main__":
    c = Combiner()
    c.calculatepriceandtime()
    c.disssb()
    c.dishistory()
    c.dishistorytime()

