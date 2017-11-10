__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
import warnings
warnings.filterwarnings("ignore")
from constants import pricing_tpch
from integration_tpch import QueryLister
from integration_tpch import dbutils
from sets import Set
from timeit import default_timer
import pickle
import datetime
from matplotlib import rc_file
rc_file('../experiments/matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 4.44, 1.95
mpl.rcParams['xtick.labelsize'] = 5
mpl.rcParams['legend.fontsize'] = 7
class Combiner:


    q = QueryLister.Query()
    print "loading ss"
    with open('supportsetnew99999.txt', 'rb') as f:
        support_set = pickle.load(f)
    print "loaded ss"
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
    landarr = Set([])
    naive = []
    with_sampling = []
    qt = []
    print "beginning cleanup"
    data = [[0 for i in range(0, 22)] for j in range(pricing_tpch.support_count[0])]
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`lineitem_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`partsupp_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`part_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`supplier_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`orders_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`customer_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`nation_view`;')
    dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`region_view`;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `region_view` (  `r_regionkey` int(11) NOT NULL,  `r_name` char(25) NOT NULL,  `r_comment` varchar(152) NOT NULL,  PRIMARY KEY (`r_regionkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `nation_view` (  `n_nationkey` int(11) NOT NULL,  `n_name` char(25) NOT NULL,  `n_regionkey` int(11) NOT NULL,  `n_comment` varchar(152) NOT NULL,  PRIMARY KEY (`n_nationkey`),  KEY `n_regionkey` (`n_regionkey`),  CONSTRAINT `nationv_view_ibfk_1` FOREIGN KEY (`n_regionkey`) REFERENCES `region` (`r_regionkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `customer_view` (  `c_custkey` int(11) NOT NULL,  `c_name` varchar(25) NOT NULL,  `c_address` varchar(40) NOT NULL,  `c_nationkey` int(11) NOT NULL,  `c_phone` char(15) NOT NULL,  `c_acctbal` decimal(10,0) NOT NULL,  `c_mktsegment` char(10) NOT NULL,  `c_comment` varchar(117) NOT NULL,  PRIMARY KEY (`c_custkey`),  KEY `c_nationkey` (`c_nationkey`),  CONSTRAINT `customerv_view_ibfk_1` FOREIGN KEY (`c_nationkey`) REFERENCES `nation` (`n_nationkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `orders_view` (  `o_orderkey` int(11) NOT NULL,  `o_custkey` int(11) NOT NULL,  `o_orderstatus` char(1) NOT NULL,  `o_totalprice` decimal(10,0) NOT NULL,  `o_orderdate` date NOT NULL,  `o_orderpriority` char(15) NOT NULL,  `o_clerk` char(15) NOT NULL,  `o_shippriority` int(11) NOT NULL,  `o_comment` varchar(79) NOT NULL,  PRIMARY KEY (`o_orderkey`),  KEY `o_custkey` (`o_custkey`),  CONSTRAINT `orders_view_ibfkv_1` FOREIGN KEY (`o_custkey`) REFERENCES `customer` (`c_custkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `supplier_view` (  `s_suppkey` int(11) NOT NULL,  `s_name` char(25) NOT NULL,  `s_address` varchar(40) NOT NULL,  `s_nationkey` int(11) NOT NULL,  `s_phone` char(15) NOT NULL,  `s_acctbal` decimal(10,0) NOT NULL,  `s_comment` varchar(101) NOT NULL,  PRIMARY KEY (`s_suppkey`),  KEY `s_nationkey` (`s_nationkey`),  CONSTRAINT `supplierv_view_ibfk_1` FOREIGN KEY (`s_nationkey`) REFERENCES `nation` (`n_nationkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `part_view` (  `p_partkey` int(11) NOT NULL,  `p_name` varchar(55) NOT NULL,  `p_mfgr` char(25) NOT NULL,  `p_brand` char(10) NOT NULL,  `p_type` varchar(25) NOT NULL,  `p_size` int(11) NOT NULL,  `p_container` char(10) NOT NULL,  `p_retailprice` decimal(10,0) NOT NULL,  `p_comment` varchar(23) NOT NULL,  PRIMARY KEY (`p_partkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `partsupp_view` (  `ps_partkey` int(11) NOT NULL,  `ps_suppkey` int(11) NOT NULL,  `ps_availqty` int(11) NOT NULL,  `ps_supplycost` decimal(10,0) NOT NULL,  `ps_comment` varchar(199) NOT NULL,  `ps_id` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`ps_partkey`,`ps_suppkey`),  KEY `ps_suppkey` (`ps_suppkey`),  KEY `k` (`ps_id`),  CONSTRAINT `partsuppv_ibfk_1` FOREIGN KEY (`ps_partkey`) REFERENCES `part` (`p_partkey`),  CONSTRAINT `partsuppv_ibfk_2` FOREIGN KEY (`ps_suppkey`) REFERENCES `supplier` (`s_suppkey`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;')
    dbutils.DBUtils.cursor.execute('CREATE TABLE `lineitem_view` (  `l_orderkey` int(11) NOT NULL,  `l_partkey` int(11) NOT NULL,  `l_suppkey` int(11) NOT NULL,  `l_linenumber` int(11) NOT NULL,  `l_quantity` decimal(10,0) NOT NULL,  `l_extendedprice` decimal(10,0) NOT NULL,  `l_discount` decimal(10,0) NOT NULL,  `l_tax` decimal(10,0) NOT NULL,  `l_returnflag` char(1) NOT NULL,  `l_linestatus` char(1) NOT NULL,  `l_shipdate` date NOT NULL,  `l_commitdate` date NOT NULL,  `l_receiptdate` date NOT NULL,  `l_shipinstruct` char(25) NOT NULL,  `l_shipmode` char(10) NOT NULL,  `l_comment` varchar(44) NOT NULL,  `l_id` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`l_orderkey`,`l_linenumber`),  KEY `l_partkey` (`l_partkey`),  KEY `l_suppkey` (`l_suppkey`),  KEY `l_id` (`l_id`),  CONSTRAINT `lineitemv_ibfk_1` FOREIGN KEY (`l_orderkey`) REFERENCES `orders` (`o_orderkey`),  CONSTRAINT `lineitemv_ibfk_2` FOREIGN KEY (`l_partkey`) REFERENCES `part` (`p_partkey`),  CONSTRAINT `lineitemv_ibfk_3` FOREIGN KEY (`l_suppkey`) REFERENCES `supplier` (`s_suppkey`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;')
    print "ended cleanup"

    def cleanup(self):
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`lineitem_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`partsupp_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`part_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`supplier_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`orders_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`customer_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`nation_view`;')
        dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `tpch`.`region_view`;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `region_view` (  `r_regionkey` int(11) NOT NULL,  `r_name` char(25) NOT NULL,  `r_comment` varchar(152) NOT NULL,  PRIMARY KEY (`r_regionkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `nation_view` (  `n_nationkey` int(11) NOT NULL,  `n_name` char(25) NOT NULL,  `n_regionkey` int(11) NOT NULL,  `n_comment` varchar(152) NOT NULL,  PRIMARY KEY (`n_nationkey`),  KEY `n_regionkey` (`n_regionkey`),  CONSTRAINT `nationv_view_ibfk_1` FOREIGN KEY (`n_regionkey`) REFERENCES `region` (`r_regionkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `customer_view` (  `c_custkey` int(11) NOT NULL,  `c_name` varchar(25) NOT NULL,  `c_address` varchar(40) NOT NULL,  `c_nationkey` int(11) NOT NULL,  `c_phone` char(15) NOT NULL,  `c_acctbal` decimal(10,0) NOT NULL,  `c_mktsegment` char(10) NOT NULL,  `c_comment` varchar(117) NOT NULL,  PRIMARY KEY (`c_custkey`),  KEY `c_nationkey` (`c_nationkey`),  CONSTRAINT `customerv_view_ibfk_1` FOREIGN KEY (`c_nationkey`) REFERENCES `nation` (`n_nationkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `orders_view` (  `o_orderkey` int(11) NOT NULL,  `o_custkey` int(11) NOT NULL,  `o_orderstatus` char(1) NOT NULL,  `o_totalprice` decimal(10,0) NOT NULL,  `o_orderdate` date NOT NULL,  `o_orderpriority` char(15) NOT NULL,  `o_clerk` char(15) NOT NULL,  `o_shippriority` int(11) NOT NULL,  `o_comment` varchar(79) NOT NULL,  PRIMARY KEY (`o_orderkey`),  KEY `o_custkey` (`o_custkey`),  CONSTRAINT `orders_view_ibfkv_1` FOREIGN KEY (`o_custkey`) REFERENCES `customer` (`c_custkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `supplier_view` (  `s_suppkey` int(11) NOT NULL,  `s_name` char(25) NOT NULL,  `s_address` varchar(40) NOT NULL,  `s_nationkey` int(11) NOT NULL,  `s_phone` char(15) NOT NULL,  `s_acctbal` decimal(10,0) NOT NULL,  `s_comment` varchar(101) NOT NULL,  PRIMARY KEY (`s_suppkey`),  KEY `s_nationkey` (`s_nationkey`),  CONSTRAINT `supplierv_view_ibfk_1` FOREIGN KEY (`s_nationkey`) REFERENCES `nation` (`n_nationkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `part_view` (  `p_partkey` int(11) NOT NULL,  `p_name` varchar(55) NOT NULL,  `p_mfgr` char(25) NOT NULL,  `p_brand` char(10) NOT NULL,  `p_type` varchar(25) NOT NULL,  `p_size` int(11) NOT NULL,  `p_container` char(10) NOT NULL,  `p_retailprice` decimal(10,0) NOT NULL,  `p_comment` varchar(23) NOT NULL,  PRIMARY KEY (`p_partkey`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `partsupp_view` (  `ps_partkey` int(11) NOT NULL,  `ps_suppkey` int(11) NOT NULL,  `ps_availqty` int(11) NOT NULL,  `ps_supplycost` decimal(10,0) NOT NULL,  `ps_comment` varchar(199) NOT NULL,  `ps_id` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`ps_partkey`,`ps_suppkey`),  KEY `ps_suppkey` (`ps_suppkey`),  KEY `k` (`ps_id`),  CONSTRAINT `partsuppv_ibfk_1` FOREIGN KEY (`ps_partkey`) REFERENCES `part` (`p_partkey`),  CONSTRAINT `partsuppv_ibfk_2` FOREIGN KEY (`ps_suppkey`) REFERENCES `supplier` (`s_suppkey`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;')
        dbutils.DBUtils.cursor.execute('CREATE TABLE `lineitem_view` (  `l_orderkey` int(11) NOT NULL,  `l_partkey` int(11) NOT NULL,  `l_suppkey` int(11) NOT NULL,  `l_linenumber` int(11) NOT NULL,  `l_quantity` decimal(10,0) NOT NULL,  `l_extendedprice` decimal(10,0) NOT NULL,  `l_discount` decimal(10,0) NOT NULL,  `l_tax` decimal(10,0) NOT NULL,  `l_returnflag` char(1) NOT NULL,  `l_linestatus` char(1) NOT NULL,  `l_shipdate` date NOT NULL,  `l_commitdate` date NOT NULL,  `l_receiptdate` date NOT NULL,  `l_shipinstruct` char(25) NOT NULL,  `l_shipmode` char(10) NOT NULL,  `l_comment` varchar(44) NOT NULL,  `l_id` int(11) NOT NULL AUTO_INCREMENT,  PRIMARY KEY (`l_orderkey`,`l_linenumber`),  KEY `l_partkey` (`l_partkey`),  KEY `l_suppkey` (`l_suppkey`),  KEY `l_id` (`l_id`),  CONSTRAINT `lineitemv_ibfk_1` FOREIGN KEY (`l_orderkey`) REFERENCES `orders` (`o_orderkey`),  CONSTRAINT `lineitemv_ibfk_2` FOREIGN KEY (`l_partkey`) REFERENCES `part` (`p_partkey`),  CONSTRAINT `lineitemv_ibfk_3` FOREIGN KEY (`l_suppkey`) REFERENCES `supplier` (`s_suppkey`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;')
#Q4
    def Query1(self):
        self.cleanup()
        query1 = 'select l_id, o_orderkey, o_orderpriority, l_commitdate, l_receiptdate from orders, lineitem where 	o_orderdate >= date \'1993-07-01\' 	and o_orderdate < date \'1993-07-01\' + interval \'3\' month 	and l_orderkey = o_orderkey 	and l_commitdate < l_receiptdate; '
        query2 = 'select l_id, o_orderkey, o_orderpriority, l_commitdate, l_receiptdate from orders, lineitem where 	o_orderdate < date \'1993-07-01\' 	and o_orderdate > date \'1993-07-01\' + interval \'3\' month 	and l_orderkey = o_orderkey 	and l_commitdate < l_receiptdate; '
        #query3 = 'select l_id, o_orderkey, o_orderpriority, l_commitdate, l_receiptdate from orders, lineitem where 	o_orderdate >= date \'1993-07-01\' 	and o_orderdate < date \'1993-07-01\' + interval \'3\' month 	and l_orderkey = o_orderkey 	and l_commitdate >= l_receiptdate; '
        query4 = 'select o_orderkey, o_orderdate, o_orderpriority from orders'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        linout = Set([])
        oinout = Set([])
        dictorderpri = {}
        dictlipkcd = {}
        dictlipkrd = {}
        for i in range(0, len(res)):
            linout.add(res[i][0])
            oinout.add(res[i][1])
            dictorderpri[res[i][1]] = res[i][2]
            dictlipkcd[res[i][0]] = str(res[i][3])
            dictlipkrd[res[i][0]] = str(res[i][4])
        lin2out = Set([])
        oin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            lin2out.add(res[i][0])
            oin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        dictordersdate = {}
        dictorderspri = {}
        for i in range(0, len(res)):
            dictordersdate[res[i][0]] = datetime.datetime.strptime(str(res[i][1]), "%Y-%m-%d")
            dictorderspri[res[i][0]] = res[i][2]
        i = 0
        count=0
        countnohistory=0
        counthistory=0
        print "Started"
        countswap = 1
        start = default_timer()
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            ele_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
                ele_2_value = self.support_set_value[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'lineitem_view' in ele_2[0] : #not calcultating exact price, just counting!
                countswap += 1
            if self.willOutputChangeQuery1(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_2_value, ele_undo_2, linout,
                                           oinout, lin2out, oin2out , dictorderpri,
                                           dictlipkcd, dictlipkrd, dictordersdate, dictorderspri, code_changed_1, code_changed_2) == False:
                self.data[index][1] = 0
            else:
                self.data[index][1] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query5 = 'select l_id, o_orderkey, o_orderpriority, l_commitdate, l_receiptdate from orders, lineitem_view where 	o_orderdate >= date \'1993-07-01\' 	and o_orderdate < date \'1993-07-01\' + interval \'3\' month 	and l_orderkey = o_orderkey 	and l_commitdate < l_receiptdate; '
        dbutils.DBUtils.cursor.execute(query5)
        res1 = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        query7 = 'select count(*) from lineitem_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (endadhoc - beginadhoc)*(countrows + countswap)]

    def willOutputChangeQuery1(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_2_value, ele_undo_2, linout,
                                           oinout, lin2out, oin2out,  dictorderpri,
                               dictlipkcd, dictlipkrd, dictordersdate, dictorderspri, code_changed_1, code_changed_2):
        if('nation_view' in ele_1[0] or 'supplier_view'  in ele_1[0] or 'region_view'  in ele_1[0]
        or 'customer_view'  in ele_1[0] or 'partsupp_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout:
                    if 'SET l_commitdate' in ele_1[0] or 'SET l_receiptdate' in ele_1[0]:
                        cd = datetime.datetime.strptime(dictlipkcd[code_changed_1], "%Y-%m-%d" )
                        rd = datetime.datetime.strptime(dictlipkrd[code_changed_1], "%Y-%m-%d" )
                        if rd <= cd:
                            return True
                else:
                    if 'SET l_orderkey' in ele_1[0] or 'SET l_commitdate' in ele_1[0] or 'SET l_receiptdate' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                            'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'orders_view' in ele_1[0]:
                if code_changed_1 in oinout:
                    if 'o_orderpriority' in ele_1[0]:
                        return True
                    if 'o_orderdate' in ele_1[0] in ele_1[0] and ('1993-07' not in str(ele_1_value) and '1993-08' not in str(ele_1_value)
                                                      and '1993-09' not in str(ele_1_value)):
                        return True
                else:
                    if 'o_orderdate' in ele_1[0] and code_changed_1 in oin2out:
                        if '1993-07' in str(ele_1_value) or '1993-08' in str(ele_1_value) or '1993-09' not in str(ele_1_value):
                            return True
        # if ele_2 == None:
        #     if 'lineitem_view' in ele_1[0]:
        #         if code_changed_1 in linout:
        #             if 'SET l_commitdate' in ele_1[0] or 'SET l_receiptdate' in ele_1[0]:
        #                 cd = datetime.datetime.strptime(dictlipkcd[code_changed_1], "%Y-%m-%d" )
        #                 rd = datetime.datetime.strptime(dictlipkrd[code_changed_1], "%Y-%m-%d" )
        #                 if rd <= cd:
        #                     return True
        #         else:
        #             if 'SET l_orderkey' in ele_1[0] or 'SET l_commitdate' in ele_1[0] or 'SET l_receiptdate' in ele_1[0]:
        #                 dbutils.DBUtils.cursor.execute(
        #                     'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
        #                 dbutils.DBUtils.cursor.execute(ele_1[0])
        #     if 'orders_view' in ele_1[0]:
        #         if code_changed_1 in oinout:
        #             if 'o_orderpriority' in ele_1[0]:
        #                 return True
        #             if 'o_orderdate' in ele_1[0] in ele_1[0] and ('1993-07' not in str(ele_1_value) and '1993-08' not in str(ele_1_value)
        #                                               and '1993-09' not in str(ele_1_value)):
        #                 return True
        #         else:
        #             if 'o_orderdate' in ele_1[0] and code_changed_1 in oin2out:
        #                 if '1993-07' in str(ele_1_value) or '1993-08' in str(ele_1_value) or '1993-09' not in str(ele_1_value):
        #                     return True
        # else:
        #     if 'lineitem_view' in ele_1[0]:
        #         if code_changed_1 not in linout and code_changed_2 not in linout:
        #             if 'SET l_commitdate' in ele_1[0] or 'SET l_receiptdate' in ele_1[0]:
        #                 dbutils.DBUtils.cursor.execute(
        #                     'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
        #                 dbutils.DBUtils.cursor.execute(ele_1[0])
        #                 dbutils.DBUtils.cursor.execute(
        #                     'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_2))
        #                 dbutils.DBUtils.cursor.execute(ele_2[0])
        #         else:
        #             if 'SET l_orderkey' in ele_1[0]:
        #                 if code_changed_1 in linout:
        #                     if code_changed_2 in linout:
        #                         None
        #                     else:
        #                         if dictordersdate[ele_1_value] < datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             or dictordersdate[ele_1_value] >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             + relativedelta(months=+3) or dictorderpri[ele_1_value] != dictorderpri[ele_2_value]:
        #                             return True
        #                 else:
        #                     if dictordersdate[ele_2_value] < datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             or dictordersdate[ele_2_value] >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             + relativedelta(months=+3) or dictorderpri[ele_1_value] != dictorderpri[ele_2_value]:
        #                             return True
        #     if 'orders_view' in ele_1[0]:
        #         if 'SET o_orderpriority' in ele_1[0]:
        #             return True
        #         if 'SET o_orderdate' in ele_1[0]:
        #             if code_changed_1 not in oinout and code_changed_2 not in oinout:
        #                 if code_changed_1 in oin2out:
        #                     if code_changed_2 not in oin2out:
        #                         if ele_1_value < datetime.datetime.strptime("1993-07-01", "%Y-%m-%d").date() \
        #                             or ele_1_value >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d").date() \
        #                             + relativedelta(months=+3):
        #                             return True
        #                 else:
        #                     if code_changed_2 in oin2out:
        #                         if ele_2_value < datetime.datetime.strptime("1993-07-01", "%Y-%m-%d").date() \
        #                             or ele_2_value >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d").date() \
        #                             + relativedelta(months=+3):
        #                             return True
        #             else:
        #                 if code_changed_1 in oinout:
        #                     if code_changed_2 in oinout:
        #                         None
        #                     else:
        #                         if dictorderspri[code_changed_1] != dictorderspri[code_changed_2] or \
        #                             (dictorderspri[code_changed_1] == dictorderspri[code_changed_2] and (ele_1_value <
        #                             datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             or ele_1_value >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") + relativedelta(months=+3))):
        #                                 return True
        #                 else:
        #                     if code_changed_2 in oinout:
        #                         if dictorderspri[code_changed_1] != dictorderspri[code_changed_2] or \
        #                             (dictorderspri[code_changed_1] == dictorderspri[code_changed_2] and (ele_1_value <
        #                             datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") \
        #                             or ele_1_value >= datetime.datetime.strptime("1993-07-01", "%Y-%m-%d") + relativedelta(months=+3))):
        #                                 return True
        return False
#Q5
    def Query2(self):
        self.cleanup()
        query1 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        query2 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name != \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        query3 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate < date \'1994-01-01\' 	and o_orderdate >= date \'1994-01-01\' + interval \'1\' year'
        query4 = 'select r_regionkey from region WHERE r_name = \'ASIA\''
        query5 = 'select n_nationkey from nation, region where n_regionkey = r_regionkey and r_name = \'ASIA\''
        query6 = 'select s_suppkey from nation, region, supplier where s_nationkey = n_nationkey and  n_regionkey = r_regionkey and r_name = \'ASIA\''
        rasia = Set([])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            rasia.add(res[i][0])
        nasia = Set([])
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            nasia.add(res[i][0])
        sasia = Set([])
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            sasia.add(res[i][0])
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        linout = Set([])
        oinout = Set([])
        cinout = Set([])
        sinout = Set([])
        ninout = Set([])
        rinout = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
            oinout.add(res[i][1])
            cinout.add(res[i][2])
            sinout.add(res[i][3])
            ninout.add(res[i][4])
            rinout.add(res[i][5])
        rin2out = Set([])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            rin2out.add(res[i][0])
        oin3out = Set([])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        for i in range(0, len(res)):
            oin3out.add(res[i][0])
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        start = default_timer()
        countswap = 0
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            code_changed_2 = None
            ele_2_value = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
                code_changed_2 = self.support_set_pk[i + 1][0]
                ele_2_value = self.support_set_value[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None:
                countswap += 1
            if self.willOutputChangeQuery2(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout,
                                           oinout, cinout, sinout, ninout, rinout, rin2out, oin3out,
                                           rasia, nasia, sasia,code_changed_1, code_changed_2) == False:
                self.data[index][2] = 0
            else:
                self.data[index][2] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        query2 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer_view, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        query4 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	lineitem_view, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        query5 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier_view, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        query6 = 'select 	l_id,o_orderkey,c_custkey,s_suppkey,n_nationkey,r_regionkey from 	customer, 	orders, 	(select * from lineitem limit 100000) as lineitem, 	supplier, 	nation_view, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year'
        beginadhoc1 = default_timer()
        dbutils.DBUtils.cursor.execute(query2)
        res2 = dbutils.DBUtils.cursor.fetchall()
        beginadhoc2 = default_timer()
        dbutils.DBUtils.cursor.execute(query4)
        res4 = dbutils.DBUtils.cursor.fetchall()
        beginadhoc3 = default_timer()
        dbutils.DBUtils.cursor.execute(query5)
        res5 = dbutils.DBUtils.cursor.fetchall()
        beginadhoc4 = default_timer()
        dbutils.DBUtils.cursor.execute(query6)
        res6 = dbutils.DBUtils.cursor.fetchall()
        endadhoc4 = default_timer()
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        query7 = 'SELECT  (SELECT COUNT(*) FROM   customer_view) AS count1,(SELECT COUNT(*) FROM   lineitem_view),(SELECT COUNT(*) FROM   supplier_view),(SELECT COUNT(*) FROM   nation_view) AS count2 FROM dual;'
        dbutils.DBUtils.cursor.execute(query7)
        res = dbutils.DBUtils.cursor.fetchall()
        print res
        countrows1 = max(res[0][0],1)
        countrows2 = max(res[0][1],1)
        countrows3 = max(res[0][2],1)
        countrows4 = max(res[0][3],1)
        print "time : ", default_timer() - start
        print "countswap : ", countswap
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (beginadhoc2 - beginadhoc1)*countrows1 +
                (beginadhoc3 - beginadhoc2)*countrows2 + (beginadhoc4 - beginadhoc3)*countrows3 + (endadhoc4 - beginadhoc4)*countrows4]

    def willOutputChangeQuery2(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout,
                                           oinout, cinout, sinout, ninout, rinout, rin2out, oin3out, rasia, nasia, sasia,
                               code_changed_1, code_changed_2):
        if('partsupp_view' in ele_1[0] or 'part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout and ('l_extendedprice' in ele_1[0] or 'l_discount' in ele_1[0]):
                    return True
                else:
                    if 'l_orderkey' in ele_1[0] or 'l_suppkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'orders_view' in ele_1[0]:
                if code_changed_1 in oinout:
                    if 'o_orderdate' in ele_1[0] and ('1994' not in str(ele_1_value)):
                        return True
                else:
                    if 'o_orderdate' in ele_1[0]:
                        if code_changed_1 in oin3out:
                            if '1994' in str(ele_1_value):
                                return True
            if 'customer_view' in ele_1[0]:
                if 'c_nationkey' in ele_1[0]:
                    dbutils.DBUtils.cursor.execute(
                            'insert ignore into customer_view select * from customer where c_custkey = ' + str(code_changed_1))
                    dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'supplier_view' in ele_1[0]:
                if 's_nationkey' in ele_1[0]:
                    if code_changed_1 in sinout and ele_1_value not in sasia:
                        return True
                    else:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into supplier_view select * from supplier where s_suppkey = ' + str(code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'nation_view' in ele_1[0]:
                if code_changed_1 in ninout:
                    if 'n_name' in ele_1[0]:
                        return True
                    if 'n_regionkey' in ele_1[0]:
                        if ele_1_value not in nasia:
                            return True
                else:
                    dbutils.DBUtils.cursor.execute(
                            'insert ignore into nation_view select * from nation where n_nationkey = ' + str(code_changed_1))
                    dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'region_view' in ele_1[0]:
                if code_changed_1 in rinout and 'r_name' in ele_1[0]:
                    return True
                else:
                    if 'r_name' in ele_1[0]:
                        if code_changed_1 in rin2out:
                            if 'ASIA' in ele_1_value:
                                return True
        return False
#Q6
    def Query3(self):
        query1 = 'select 	l_id from 	lineitem where 	l_shipdate >= date \'1994-01-01\' 	and l_shipdate < date \'1994-01-01\' + interval \'1\' year 	and l_discount between 0.05 and 0.07 	and l_quantity < 24; '
        query2 = 'select 	l_id from 	lineitem where 	l_shipdate < date \'1994-01-01\' 	and l_shipdate >= date \'1994-01-01\' + interval \'1\' year 	and l_discount between 0.05 and 0.07 	and l_quantity < 24; '
        query3 = 'select 	l_id from 	lineitem where 	l_shipdate >= date \'1994-01-01\' 	and l_shipdate < date \'1994-01-01\' + interval \'1\' year 	and l_discount not between 0.05 and 0.07 	and l_quantity < 24; '
        query4 = 'select 	l_id from 	lineitem where 	l_shipdate >= date \'1994-01-01\' 	and l_shipdate < date \'1994-01-01\' + interval \'1\' year 	and l_discount between 0.05 and 0.07 	and l_quantity >= 24; '
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        linout = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        lin2out = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        lin3out = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        lin4out = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        countswap=0
        start = default_timer()
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'lineitem' in ele_2[0]:
                countswap += 1
            if self.willOutputChangeQuery3(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2,
                                           linout, lin2out, lin3out, lin4out, code_changed_1) == False:
                self.data[index][3] = 0
            else:
                self.data[index][3] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (endq - beginq)*countswap]

    def willOutputChangeQuery3(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2,
                                           linout, lin2out, lin3out, lin4out, code_changed_1):
        if('partsupp' in ele_1[0] or 'nation' in ele_1[0] or 'region' in ele_1[0] or 'customer' in ele_1[0] or 'supplier' in ele_1[0]
           or 'orders' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'lineitem_sample' in ele_1[0] or 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout:
                    if 'l_extendedprice' in ele_1[0] or 'l_discount' in ele_1[0]:
                        return True
                else:
                    if 'l_shipdate' in ele_1[0] and code_changed_1 in lin2out:
                        sd = datetime.datetime.strptime(ele_1_value, "%Y-%m-%d" )
                        ed = datetime.datetime.strptime("1994-01-01", "%Y-%m-%d" )
                        if sd == ed:
                            return True
                    if 'l_quantity' in ele_1[0] and code_changed_1 in lin4out:
                        if ele_1_value <= 24:
                            return True
                    if 'l_discount' in ele_1[0] and code_changed_1 in lin3out:
                        if ele_1_value <= 0.07 and ele_1_value >= 0.05:
                            return True
        return False
#Q12
    def Query4(self):
        query1 = 'select l_id, o_orderkey,l_shipmode,o_orderpriority, o_orderkey	 from 	orders, 	lineitem where 	o_orderkey = l_orderkey 	and (l_shipmode = \'MAIL\' or l_shipmode = \'SHIP\') 	and l_commitdate < l_receiptdate 	and l_shipdate < l_commitdate 	and l_receiptdate >= date \'1994-01-01\' 	and l_receiptdate < date \'1994-01-01\' + interval \'1\' year'
        query2 = 'select l_id, o_orderkey,l_shipmode,o_orderpriority, o_orderkey	 from 	orders, 	lineitem where 	o_orderkey = l_orderkey 	and (l_shipmode != \'MAIL\' and l_shipmode != \'SHIP\') 	and l_commitdate < l_receiptdate 	and l_shipdate < l_commitdate 	and l_receiptdate >= date \'1994-01-01\' 	and l_receiptdate < date \'1994-01-01\' + interval \'1\' year'
        query3 = 'select l_id, o_orderkey,l_shipmode,o_orderpriority, o_orderkey	 from 	orders, 	lineitem where 	o_orderkey = l_orderkey 	and (l_shipmode = \'MAIL\' or l_shipmode = \'SHIP\') 	and l_commitdate < l_receiptdate 	and l_shipdate < l_commitdate 	and l_receiptdate < date \'1994-01-01\' 	and l_receiptdate >= date \'1994-01-01\' + interval \'1\' year'
        print "starting adhoc"
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        print "ending 1"
        linout = Set([])
        oinout = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
            oinout.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        print "ending 2"
        lin2out = Set([])
        oin2out = Set([])
        for i in range(0, len(res)):
            lin2out.add(res[i][0])
            oin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        print "ending 3"
        lin3out = Set([])
        oin3out = Set([])
        for i in range(0, len(res)):
            lin3out.add(res[i][0])
            oin3out.add(res[i][1])
        print "ending adhoc"
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        start = default_timer()
        countswap = 0
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'lineitem' in ele_2[0]:
                countswap += 1
            if self.willOutputChangeQuery4(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout, oinout,
                                           lin2out, oin2out, lin3out, oin3out, code_changed_1) == False:
                self.data[index][4] = 0
            else:
                self.data[index][4] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query4 = 'select l_id, o_orderkey	 from 	orders, 	lineitem_view where 	o_orderkey = l_orderkey 	and (l_shipmode = \'MAIL\' or l_shipmode = \'SHIP\') 	and l_commitdate < l_receiptdate 	and l_shipdate < l_commitdate 	and l_receiptdate >= date \'1994-01-01\' 	and l_receiptdate < date \'1994-01-01\' + interval \'1\' year'
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        query7 = 'select count(*) from lineitem_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (endq - beginq)*(countrows+countswap)]

    def willOutputChangeQuery4(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout, oinout,
                                           lin2out, oin2out, lin3out, oin3out, code_changed_1):
        if('partsupp' in ele_1[0] or 'part' in ele_1[0] or 'nation' in ele_1[0] or 'region' in ele_1[0] or 'customer' in ele_1[0] or 'supplier' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout:
                    if 'l_shipmode' in ele_1[0] and (ele_1_value not in ['MAIL', 'SHIP'] or ele_undo_1_value not in ['MAIL','SHIP']):
                        return True
                    if 'l_receiptdate' in ele_1[0] and '1994' not in str(ele_1_value):
                        return True
                else:
                    if 'l_shipmode' in ele_1[0] and code_changed_1 in lin2out and ('MAIL' in ele_1_value or 'SHIP' in ele_1_value):
                        return True
                    if 'l_receiptdate' in ele_1[0] and code_changed_1 in lin3out and ('1994' in ele_1_value):
                        return True
                    if 'l_commitdate' in ele_1[0] or 'l_shipdate' in ele_1[0] or 'l_orderkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])
            if 'orders_view' in ele_1[0]:
                if code_changed_1 in oinout:
                    if 'o_orderpriority' in ele_1[0] and ('1-' not in ele_1_value or '2-' not in ele_1_value):
                        return True

        return False
#Q16
    def Query5(self):
        query1 = 'select 	p_partkey, ps_id from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand <> \'Brand#45\' 	and p_type not like \'MEDIUM POLISHED%\' 	and p_size in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey not in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	)'
        query2 = 'select 	p_partkey, ps_id from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand = \'Brand#45\' 	and p_type not like \'MEDIUM POLISHED%\' 	and p_size in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey not in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	)'
        query3 = 'select 	p_partkey, ps_id from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand <> \'Brand#45\' 	and p_type like \'MEDIUM POLISHED%\' 	and p_size in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey not in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	)'
        query4 = 'select 	p_partkey, ps_id from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand <> \'Brand#45\' 	and p_type not like \'MEDIUM POLISHED%\' 	and p_size not in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey not in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	)'
        query6 = 'select 	p_partkey, ps_id from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand <> \'Brand#45\' 	and p_type not like \'MEDIUM POLISHED%\' 	and p_size not in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	)'
        query5 = 'select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\''
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        pinout = Set([])
        psinout = Set([])
        for i in range(0, len(res)):
            pinout.add(res[i][0])
            psinout.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        pin2out = Set([])
        psin2out = Set([])
        for i in range(0, len(res)):
            pin2out.add(res[i][0])
            psin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        pin3out = Set([])
        psin3out = Set([])
        for i in range(0, len(res)):
            pin3out.add(res[i][0])
            psin3out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        pin4out = Set([])
        psin4out = Set([])
        for i in range(0, len(res)):
            pin4out.add(res[i][0])
            psin4out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query6)
        res = dbutils.DBUtils.cursor.fetchall()
        psin6out = Set([])
        for i in range(0, len(res)):
            psin6out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        scomment = Set([])
        for i in range(0, len(res)):
            scomment.add(res[i][0])
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        start = default_timer()
        countswap = 0
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'part' in ele_2[0]:
                countswap += 1
            if self.willOutputChangeQuery5(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, psinout,
                                           pin2out, psin2out, pin3out, psin3out, pin4out, psin4out,psin6out, scomment, code_changed_1) == False:
                self.data[index][5] = 0
            else:
                self.data[index][5] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (default_timer() - start)*countswap]

    def willOutputChangeQuery5(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, psinout,
                                           pin2out, psin2out, pin3out, psin3out, pin4out, psin4out, psin6out, scomment, code_changed_1):
        if('nation' in ele_1[0] or 'region' in ele_1[0] or 'customer' in ele_1[0] or 'supplier' in ele_1[0] or 'orders' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'part_view' in ele_1[0]:
                if code_changed_1 in pinout:
                    if 'p_brand' in ele_1[0] or 'p_type' in ele_1[0] or 'p_size' in ele_1[0]:
                        return True
                else:
                    if 'p_brand' in ele_1[0] and code_changed_1 in pin2out and 'Brand#45' in ele_1_value:
                        return True
                    if 'p_type' in ele_1[0] and code_changed_1 in pin3out and str(ele_1_value).startswith('MEDIUM POLISHED'):
                        return True
                    if 'p_size' in ele_1[0] and code_changed_1 in pin4out and ele_1_value in [49, 14, 23, 45, 19, 3, 36, 9]:
                        return True
            if 'partsupp' in ele_1[0]:
                if code_changed_1 in psinout:
                    if 'ps_suppkey' in ele_1[0] and ele_1_value not in scomment:
                        return True
                else:
                    if 'ps_suppkey' in ele_1[0] and code_changed_1 in psin6out and ele_1_value in scomment:
                        return True


        return False
#Q17
    def Query6(self):
        query1 = 'select 	l_id, p_partkey from 	lineitem, 	part where 	p_partkey = l_partkey 	and p_brand = \'Brand#23\' 	and p_container = \'MED BOX\' 	and l_quantity < 5.10736 '
        query2 = 'select 	l_id, p_partkey from 	lineitem, 	part where 	p_partkey = l_partkey 	and p_brand != \'Brand#23\' 	and p_container = \'MED BOX\' 	and l_quantity < 5.10736'
        query3 = 'select 	l_id, p_partkey from 	lineitem, 	part where 	p_partkey = l_partkey 	and p_brand = \'Brand#23\' 	and p_container != \'MED BOX\' 	and l_quantity < 5.10736'
        query4 = 'select 	l_id, p_partkey from 	lineitem, 	part where 	p_partkey = l_partkey 	and p_brand = \'Brand#23\' 	and p_container = \'MED BOX\' 	and l_quantity >= 5.10736'
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        pinout = Set([])
        linout = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
            pinout.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        pin2out = Set([])
        lin2out = Set([])
        for i in range(0, len(res)):
            lin2out.add(res[i][0])
            pin2out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        pin3out = Set([])
        lin3out = Set([])
        for i in range(0, len(res)):
            lin3out.add(res[i][0])
            pin3out.add(res[i][1])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        pin4out = Set([])
        lin4out = Set([])
        for i in range(0, len(res)):
            lin4out.add(res[i][0])
            pin4out.add(res[i][1])

        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        countswap=0
        start = default_timer()
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'lineitem' in ele_2[0]:
                countswap += 1
            if self.willOutputChangeQuery6(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, linout,
                                           pin2out, lin2out, pin3out, lin3out, pin4out, lin4out, code_changed_1) == False:
                self.data[index][6] = 0
            else:
                self.data[index][6] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        beginadhoc = default_timer()
        query5 = 'select 	l_id, p_partkey from 	lineitem_view, 	part where 	p_partkey = l_partkey 	and p_brand = \'Brand#23\' 	and p_container = \'MED BOX\' 	and l_quantity < 5.10736 '
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        endadhoc = default_timer()
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        query7 = 'select count(*) from lineitem_view;'
        dbutils.DBUtils.cursor.execute(query7)
        countrows = max(dbutils.DBUtils.cursor.fetchall()[0][0],1)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (endadhoc - beginadhoc)*(countrows+countswap)]

    def willOutputChangeQuery6(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, linout,
                                           pin2out, lin2out, pin3out, lin3out, pin4out, lin4out, code_changed_1):
        if('nation' in ele_1[0] or 'partsupp' in ele_1[0] or 'region' in ele_1[0] or 'customer' in ele_1[0] or 'supplier' in ele_1[0] or 'orders' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'part_view' in ele_1[0]:
                if code_changed_1 in pinout:
                    if 'p_brand' in ele_1[0] or 'p_container' in ele_1[0]:
                        return True
                else:
                    if 'p_brand' in ele_1[0] and code_changed_1 in pin2out and 'Brand#23' in ele_1_value:
                        return  True
                    if 'p_container' in ele_1[0] and code_changed_1 in pin3out and 'MED BOX' == ele_1_value:
                        return True

            if 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout:
                    if 'l_extendedprice' in ele_1[0]:
                        return True
                    if 'l_quantity' in ele_1[0]:
                        if ele_1_value > 5.10736:
                            return True
                else:
                    if 'l_quantity' in ele_1[0] and code_changed_1 in lin4out and ele_1_value < 5.10736:
                        return True
                    if 'l_partkey' in ele_1[0]:
                        dbutils.DBUtils.cursor.execute(
                                'insert ignore into lineitem_view select * from lineitem where l_id = ' + str(code_changed_1))
                        dbutils.DBUtils.cursor.execute(ele_1[0])


        return False
#Q1
    def Query8(self):
        query1 = 'select  l_id from 	lineitem where 	l_shipdate <= date \'1998-09-01\''
        query2 = 'select  l_id from 	lineitem where 	l_shipdate > date \'1998-09-01\''
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        linout = Set([])
        for i in range(0, len(res)):
            linout.add(res[i][0])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        lin2out = Set([])
        for i in range(0, len(res)):
            lin2out.add(res[i][0])
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        countswap=0
        start = default_timer()
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and 'lineitem' in ele_2[0]:
                countswap += 1
            if self.willOutputChangeQuery8(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout,
                                           lin2out, code_changed_1) == False:
                self.data[index][8] = 0
            else:
                self.data[index][8] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (default_timer() - start)*countswap]

    def willOutputChangeQuery8(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, linout,
                                           lin2out, code_changed_1):
        if('nation_view' in ele_1[0] or 'region_view' in ele_1[0] or 'customer_view' in ele_1[0] or 'supplier_view' in ele_1[0] or 'orders_view' in ele_1[0] or 'part_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'lineitem_view' in ele_1[0]:
                if code_changed_1 in linout:
                    if 'l_returnflag' in ele_1[0] or 'l_linestatus' in ele_1[0] or 'l_quantity' in ele_1[0]\
                             or 'l_extendedprice' in ele_1[0] or 'l_discount' in ele_1[0] or 'l_tax' in ele_1[0]\
                            or 'l_quantity' in ele_1[0]:
                        return True
                    if 'l_shipdate' in ele_1[0]:
                        nd = datetime.datetime.strptime(ele_1_value, "\'%Y-%m-%d\'" )
                        od = datetime.datetime.strptime('1998-09-01', "%Y-%m-%d" )
                        if nd > od:
                            return True
                else:
                    if 'l_shipdate' in ele_1[0]:
                        if code_changed_1 in lin2out:
                            nd = datetime.datetime.strptime(ele_1_value, "\'%Y-%m-%d\'" )
                            od = datetime.datetime.strptime('1998-09-01', "%Y-%m-%d" )
                            if nd <= od:
                                return True
        return False

#Q2
    def Query10(self):
        query1 = 'select p_partkey,s_suppkey,ps_id,n_nationkey,r_regionkey,s_acctbal,s_name,n_name	 from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size = 15 	and p_type like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'EUROPE\' 	and ps_supplycost = 100 limit 100; '
        query2 = 'select p_partkey,s_suppkey,ps_id,n_nationkey,r_regionkey,s_acctbal,s_name,n_name	 from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size != 15 	and p_type like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'EUROPE\' 	and ps_supplycost = 100 limit 100; '
        query3 = 'select p_partkey,s_suppkey,ps_id,n_nationkey,r_regionkey,s_acctbal,s_name,n_name	 from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size = 15 	and p_type not like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'EUROPE\' 	and ps_supplycost = 100 limit 100; '
        query4 = 'select p_partkey,s_suppkey,ps_id,n_nationkey,r_regionkey,s_acctbal,s_name,n_name	 from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size = 15 	and p_type like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name != \'EUROPE\' 	and ps_supplycost = 100 limit 100; '
        query5 = 'select p_partkey,s_suppkey,ps_id,n_nationkey,r_regionkey,s_acctbal,s_name,n_name	 from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size = 15 	and p_type like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'EUROPE\' 	and ps_supplycost != 100 limit 100; '
        beginq = default_timer()
        dbutils.DBUtils.cursor.execute(query1)
        res = dbutils.DBUtils.cursor.fetchall()
        endq = default_timer()
        pinout = Set([])
        sinout = Set([])
        psinout = Set([])
        ninout = Set([])
        rinout = Set([])
        for i in range(0, len(res)):
            pinout.add(res[i][0])
            sinout.add(res[i][1])
            psinout.add(res[i][2])
            ninout.add(res[i][3])
            rinout.add(res[i][4])
        dbutils.DBUtils.cursor.execute(query2)
        res = dbutils.DBUtils.cursor.fetchall()
        pin2out = Set([])
        sin2out = Set([])
        psin2out = Set([])
        nin2out = Set([])
        rin2out = Set([])
        for i in range(0, len(res)):
            pin2out.add(res[i][0])
            sin2out.add(res[i][1])
            psin2out.add(res[i][2])
            nin2out.add(res[i][3])
            rin2out.add(res[i][4])
        dbutils.DBUtils.cursor.execute(query3)
        res = dbutils.DBUtils.cursor.fetchall()
        pin3out = Set([])
        sin3out = Set([])
        psin3out = Set([])
        nin3out = Set([])
        rin3out = Set([])
        for i in range(0, len(res)):
            pin3out.add(res[i][0])
            sin3out.add(res[i][1])
            psin3out.add(res[i][2])
            nin3out.add(res[i][3])
            rin3out.add(res[i][4])
        dbutils.DBUtils.cursor.execute(query4)
        res = dbutils.DBUtils.cursor.fetchall()
        pin4out = Set([])
        sin4out = Set([])
        psin4out = Set([])
        nin4out = Set([])
        rin4out = Set([])
        for i in range(0, len(res)):
            pin4out.add(res[i][0])
            sin4out.add(res[i][1])
            psin4out.add(res[i][2])
            nin4out.add(res[i][3])
            rin4out.add(res[i][4])
        dbutils.DBUtils.cursor.execute(query5)
        res = dbutils.DBUtils.cursor.fetchall()
        pin5out = Set([])
        sin5out = Set([])
        psin5out = Set([])
        nin5out = Set([])
        rin5out = Set([])
        for i in range(0, len(res)):
            pin5out.add(res[i][0])
            sin5out.add(res[i][1])
            psin5out.add(res[i][2])
            nin5out.add(res[i][3])
            rin5out.add(res[i][4])
        i = 0
        count = 0
        countnohistory=0
        counthistory=0
        countswap = 0
        start = default_timer()
        while (i < len(self.support_set)):
            ele_2 = None
            ele_undo_2 = None
            index = self.support_set[i][1]
            if i != len(self.support_set)-1 and self.support_set[i][1] == self.support_set[i+1][1]:
                ele_2 = self.support_set[i + 1]
                ele_undo_2 = self.support_set_undo[i + 1]
            ele_1 = self.support_set[i]
            ele_undo_1 = self.support_set_undo[i]
            ele_undo_1_value = self.support_set_undo_value[i]
            ele_1_value = self.support_set_value[i]
            code_changed_1 = self.support_set_pk[i][0]
            if ele_2 != None and ('part' in ele_2[0] or 'region' in ele_2[0] or 'supplier' in ele_2[0]):
                countswap += 1
            if self.willOutputChangeQuery10(ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, sinout, psinout,
                                            ninout, rinout, pin2out, sin2out, psin2out, nin2out, rin2out,
                                            pin3out, sin3out, psin3out, nin3out, rin3out,
                                            pin4out, sin4out, psin4out, nin4out, rin4out,
                                            pin5out, sin5out, psin5out, nin5out, rin5out,code_changed_1) == False:
                self.data[index][10] = 0
            else:
                self.data[index][10] = 1
                count += 1
                countnohistory += 1
                if i not in self.landarr:
                    counthistory += 1
                    self.landarr.add(i)
            if  i != len(self.support_set)-1 and  self.support_set[i][1] == self.support_set[i+1][1]:
                i = i + 2
            else:
                i = i + 1
        print "time : ", default_timer() - start
        print "count : ", float(countnohistory)/len(self.support_set), float(counthistory)/len(self.support_set)
        return [default_timer() - start, endq - beginq, (default_timer() - start)*countswap]

    def willOutputChangeQuery10(self, ele_1, ele_undo_1, ele_undo_1_value, ele_1_value, ele_2, ele_undo_2, pinout, sinout, psinout,
                                            ninout, rinout, pin2out, sin2out, psin2out, nin2out, rin2out,
                                            pin3out, sin3out, psin3out, nin3out, rin3out,
                                            pin4out, sin4out, psin4out, nin4out, rin4out,
                                            pin5out, sin5out, psin5out, nin5out, rin5out,code_changed_1):
        if('lineitem_view' in ele_1[0] or 'orders_view' in ele_1[0] or 'customer_view' in ele_1[0]):
            return False
        if ele_2 == None:
            if 'part_view' in ele_1[0]:
                if code_changed_1 in pinout:
                    if 'p_mfgr' in ele_1[0] or 'p_size' in ele_1[0]:
                        return True
                    if 'p_type' in ele_1[0] and 'BRASS' not in ele_1_value:
                        return True
                else:
                    if 'p_size' in ele_1[0] and code_changed_1 in pin2out and ele_1_value == 15:
                        return True
                    if 'p_type' in ele_1[0] and code_changed_1 in pin3out and 'BRASS' not in ele_1_value:
                        return True
            if 'supplier_view' in ele_1[0]:
                if code_changed_1 in sinout:
                    if 's_address' in ele_1[0] or 's_phone' in ele_1[0] or 's_comment' in ele_1[0] or 's_acctbal' in ele_1[0]:
                        return True
            if 'partsupp_view' in ele_1[0]:
                if code_changed_1 in psinout:
                    if 'ps_supplycost' in ele_1[0]:
                        return True
                else:
                    if 'ps_supplycost' in ele_1[0] and code_changed_1 in psin5out and ele_1_value == 100:
                        return True
            if 'region_sample' in ele_1[0]:
                if code_changed_1 in rinout:
                    if 'r_name' in ele_1[0]:
                        return True
                else:
                    if 'r_name' in ele_1[0] and code_changed_1 in rin4out and 'EUROPE' == ele_1_value:
                        return True
        return False

    def convertToString(self, queries):
        str = ''
        for i in range(0, len(queries)):
            str = str +  queries[i][0] + '\n'
        return str


    def calculatetime(self):
        queries = [
                    'Query1','Query2','Query3','Query4','Query5','Query6','Query8','Query10'
                   ]
        m = globals()['Combiner']()
        for i in range(0, len(queries)):
            output = getattr(m, queries[i])()
            self.with_sampling.append(output[0])
            self.qt.append(output[1])
            self.naive.append(output[2])

    def disbartpch(self):
        fig, ax = plt.subplots()
        ax.set_yscale('log')
        ax.set_ylim([0.05,100000])
        ax.set_xlim([0, 7])
        width = 0.2
        ax.xaxis.set_ticks([x + width for x in range(1,10)])
        ax.set_xticklabels(['$Q1$','$Q2$','$Q4$','$Q5$','$Q6$','$Q11$','$Q12$','$Q17$'])
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
        ax.bar([x - 0.5*width for x in range(1,9)], self.naive, width, color='blueviolet',  linewidth=0.5, bottom = 0)
        ax.bar([x + 0.5*width for x in range(1,9)], self.with_sampling, width, color='dodgerblue', linewidth=0.5, hatch='////////////////')
        ax.bar([x + 1.5*width for x in range(1,9)], self.qt, width, color='darkorange', linewidth=0.5, hatch='\\\\\\\\\\\\\\\\\\')
        plt.ylabel("Time in s")
        plt.xlabel("Query")
        lgd = plt.legend(['no batching','with batching', 'query execution time'], loc='upper right', ncol=3, bbox_to_anchor=(1, 1.23))
        plt.savefig('barcharttpchtimetest.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')




if __name__ == "__main__":
    c = Combiner()
    c.calculatetime()
    c.disbartpch()

    

