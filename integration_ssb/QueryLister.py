__author__ = 'shaleen'

from integration_ssb import dbutils

class Query:

    def generateQueries(self):

        ret_arr = []

        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder_discretized , dwdate where lo_orderdate = d_datekey and d_year = 1995'
                            ' and lo_discount between 1 and 10 '
                            ' and lo_quantity < 50;'])
        ret_arr.append(['select sum(lo_revenue), d_year, p_brand1 from lineorder_discretized , dwdate , part_discretized , supplier_discretized '
                        ' where lo_orderdate = d_datekey and lo_partkey = p_partkey'
                        ' and lo_suppkey = s_suppkey and p_category = \'MFGR#12\' and s_region = \'AMERICA\''
                        ' group by d_year, p_brand1 order by d_year, p_brand1;'])
        ret_arr.append(['select c_nation, s_nation, d_year, sum(lo_revenue) as revenue from customer_discretized , lineorder_discretized, supplier_discretized , dwdate '
                        ' where lo_custkey = c_custkey'
                        ' and lo_suppkey = s_suppkey'
                        ' and lo_orderdate = d_datekey'
                        ' and c_region = \'ASIA\' and s_region = \'ASIA\' and d_year >= 1992 and d_year <= 1997 '
                        ' group by c_nation, s_nation, d_year order by d_year asc, revenue desc;'])
        ret_arr.append(['select d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit from dwdate, customer_discretized, supplier_discretized, part_discretized, lineorder_discretized where lo_custkey = c_custkey'
                        ' and lo_suppkey = s _suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' '
                        ' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') group by d_year, c_nation order by '
                        ' d_year, c_nation'])
        return ret_arr


    def generateQueriesNonDiscretized(self):

        ret_arr = []

        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1995'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 50;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder, dwdate where lo_orderdate = d_datekey and d_yearmonthnum = '
                        '199401 and lo_discount between  4 and 6 and lo_quantity between 26 and 35;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder, dwdate where lo_orderdate = d_datekey and d_weeknuminyear = '
                        '6 and d_year = 1994 and lo_discount between 5 and 7 and lo_quantity between 26 and 35; '])




        ret_arr.append(['select sum(lo_revenue), d_year, p_brand1 from lineorder , dwdate , part , supplier '
                        ' where lo_orderdate = d_datekey and lo_partkey = p_partkey'
                        ' and lo_suppkey = s_suppkey and p_category = \'MFGR#12\' and s_region = \'AMERICA\''
                        ' group by d_year, p_brand1 order by d_year, p_brand1;'])
        ret_arr.append(['select sum(lo_revenue), d_year, p_brand1 from lineorder, dwdate, part, supplier where lo_orderdate = d_datekey and lo_partkey ='
                        ' p_partkey and lo_suppkey = s_suppkey and p_brand1 between \'MFGR#2221\' and \'MFGR#2228\' and s_region = \'ASIA\' '
                        'group by d_year, p_brand1 order by d_year, p_brand1; '])
        ret_arr.append(['select sum(lo_revenue), d_year, p_brand1 from lineorder, dwdate, part, supplier where lo_orderdate = d_datekey and lo_partkey = '
                        'p_partkey and lo_suppkey = s_suppkey and p_brand1 = \'MFGR#2221\' and s_region = \'EUROPE\' '
                        'group by d_year, p_brand1 order by d_year, p_brand1;'])



        ret_arr.append(['select c_nation, s_nation, d_year, sum(lo_revenue) as revenue from customer , lineorder, supplier , dwdate '
                        ' where lo_custkey = c_custkey'
                        ' and lo_suppkey = s_suppkey'
                        ' and lo_orderdate = d_datekey'
                        ' and c_region = \'ASIA\' and s_region = \'ASIA\' and d_year >= 1992 and d_year <= 1997 '
                        ' group by c_nation, s_nation, d_year order by d_year asc, revenue desc;'])
        ret_arr.append(['select c_city, s_city, d_year, sum(lo_revenue) as revenue from customer, lineorder, supplier, dwdate where lo_custkey = c_custkey '
                        'and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and c_nation = \'UNITED STATES\' and s_nation = \'UNITED STATES\' '
                        'and d_year >= 1992 and d_year <= 1997 group by c_city, s_city, d_year order by d_year asc, revenue desc;'])
        ret_arr.append(['select c_city, s_city, d_year, sum(lo_revenue) as revenue from customer, lineorder, supplier, dwdate where lo_custkey = c_custkey'
                        ' and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and '
                        '(s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_year >= 1992 and d_year <= 1997 '
                        'group by c_city, s_city, d_year order by d_year asc, revenue desc;'])
        ret_arr.append(['select c_city, s_city, d_year, sum(lo_revenue) as revenue from customer, lineorder, supplier, dwdate where lo_custkey = c_custkey '
                        'and lo_suppkey = s_suppkey and lo_orderdate = d_datekey and (c_city=\'UNITED KI1\' or c_city=\'UNITED KI5\') and '
                        '(s_city=\'UNITED KI1\' or s_city=\'UNITED KI5\') and d_yearmonth = \'Dec1997\''
                        ' group by c_city, s_city, d_year order by d_year asc, revenue desc;'])




        ret_arr.append(['select d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit from dwdate, customer, supplier, part, lineorder where lo_custkey = c_custkey'
                        ' and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' '
                        ' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') group by d_year, c_nation order by '
                        ' d_year, c_nation'])
        ret_arr.append(['select d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit from dwdate, customer, supplier, part, lineorder '
                        'where lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and '
                        'c_region = \'AMERICA\' and s_region = \'AMERICA\' and (d_year = 1997 or d_year = 1998) and '
                        '(p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') group by d_year, s_nation, p_category order by d_year, s_nation, p_category'])
        ret_arr.append(['select d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit from dwdate, customer, supplier, part, lineorder where'
                        ' lo_custkey = c_custkey and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and '
                        'c_region = \'AMERICA\' and s_nation = \'UNITED STATES\' and (d_year = 1997 or d_year = 1998) '
                        'and p_category = \'MFGR#14\' group by d_year, s_city, p_brand1 order by d_year, s_city, p_brand1'])


        return ret_arr

    def generateQueriesSequence(self):
        ret_arr = []
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 50;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1993'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 50;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1994'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 150;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1995'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 150;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1996'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 150;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1997'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 150;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1998'
                            ' and lo_discount between -1 and 10 '
                            ' and lo_quantity < 150000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1994'
                            ' and lo_discount between 3 and 50 '
                            ' and lo_quantity < 1500;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1994'
                            ' and lo_discount between 1 and 100 '
                            ' and lo_quantity < 15000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1993'
                            ' and lo_discount between 1 and 100 '
                            ' and lo_quantity < 15000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1993'
                            ' and lo_discount between 1 and 10 '
                            ' and lo_quantity < 15000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1997'
                            ' and lo_discount between 1 and 10 '
                            ' and lo_quantity < 15000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1998'
                            ' and lo_discount between 1 and 50 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1998'
                            ' and lo_discount between 1 and 50 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1998'
                            ' and lo_discount between 1 and 50 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between 1 and 75 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between 1 and 75 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between 1 and 75 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between 1 and 75 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1992'
                            ' and lo_discount between 1 and 75 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1995'
                            ' and lo_discount between 1 and 20 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1997'
                            ' and lo_discount between 1 and 40 '
                            ' and lo_quantity < 15000000;'])
        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder , dwdate where lo_orderdate = d_datekey and d_year = 1998'
                            ' and lo_discount between 60 and 80 '
                            ' and lo_quantity < 15000000;'])
        return ret_arr

    def generateLPQueries(self):
        ret_arr = []
        ret_arr.append(['select * from part '])
        ret_arr.append(['select * supplier where s_region = \'AMERICA\' '])
        ret_arr.append(['select * supplier where s_nation = \'UNITED STATES\' '])

        return ret_arr

    def populateQueryTable(self):
        str = self.generateQueriesSequence()
        dbutils.DBUtils.cursor.execute('delete from Queries')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('ALTER TABLE Queries AUTO_INCREMENT = 1')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `Queries`(`query`) VALUES (%s)', str)

    def populateLPQueryTable(self):
        str = self.generateLPQueries()
        dbutils.DBUtils.cursor.execute('delete from LPQueries')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('ALTER TABLE LPQueries AUTO_INCREMENT = 1')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('update LPQueries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `LPQueries`(`query`) VALUES (%s)', str)


if __name__ == "__main__":

    q = Query()
    q.populateQueryTable()
    #dbutils.DBUtils.cursor.execute('DROP TABLE IF EXISTS `lineitem_view`')
