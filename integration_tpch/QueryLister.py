__author__ = 'shaleen'

from integration_tpch import dbutils

class Query:

    def generateQueries(self):

        ret_arr = []

        ret_arr.append(['select sum(lo_extendedprice*lo_discount) as revenue from lineorder_discretized , dwdate where lo_orderdate = d_datekey and d_year = 1995'
                            ' and lo_discount between -1 and 10 '
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
                        ' and lo_suppkey = s_suppkey and lo_partkey = p_partkey and lo_orderdate = d_datekey and c_region = \'AMERICA\' '
                        ' and s_region = \'AMERICA\' and (p_mfgr = \'MFGR#1\' or p_mfgr = \'MFGR#2\') group by d_year, c_nation order by '
                        ' d_year, c_nation'])
        return ret_arr


    def generateQueriesNonDiscretized(self):

        ret_arr = []

        #ret_arr.append(['select 	l_returnflag, 	l_linestatus, 	sum(l_quantity) as sum_qty, 	sum(l_extendedprice) as sum_base_price, 	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price, 	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge, 	avg(l_quantity) as avg_qty, 	avg(l_extendedprice) as avg_price, 	avg(l_discount) as avg_disc, 	count(*) as count_order from 	lineitem where 	l_shipdate <= date \'1998-09-01\' group by 	l_returnflag, 	l_linestatus order by 	l_returnflag, 	l_linestatus'])
        #ret_arr.append(['select 	s_acctbal, 	s_name, 	n_name, 	p_partkey, 	p_mfgr, 	s_address, 	s_phone, 	s_comment from 	part, 	supplier, 	partsupp, 	nation, 	region where 	p_partkey = ps_partkey 	and s_suppkey = ps_suppkey 	and p_size = 15 	and p_type like \'%BRASS\' 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'EUROPE\' 	and ps_supplycost = ( 		select 			min(ps_supplycost) 		from 			partsupp, 			supplier, 			nation, 			region 		where 			p_partkey = ps_partkey 			and s_suppkey = ps_suppkey 			and s_nationkey = n_nationkey 			and n_regionkey = r_regionkey 			and r_name = \'EUROPE\' 	) order by 	s_acctbal desc, 	n_name, 	s_name, 	p_partkey limit 100;'])
        #ret_arr.append(['select 	l_orderkey, 	sum(l_extendedprice * (1 - l_discount)) as revenue, 	o_orderdate, 	o_shippriority from 	customer, 	orders, 	lineitem where 	c_mktsegment = \'BUILDING\' 	and c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and o_orderdate < date \'1995-03-15\' 	and l_shipdate > date \'1995-03-15\' group by 	l_orderkey, 	o_orderdate, 	o_shippriority order by 	revenue desc, 	o_orderdate limit 10 ; '])
        ret_arr.append(['select 	o_orderpriority, 	count(*) as order_count from 	orders,  	lineitem where 	o_orderdate >= date \'1993-07-01\' 	and o_orderdate < date \'1993-07-01\' + interval \'3\' month 	and l_orderkey = o_orderkey 	and l_commitdate < l_receiptdate group by 	o_orderpriority order by 	o_orderpriority ; '])
        ret_arr.append(['select 	n_name, 	sum(l_extendedprice * (1 - l_discount)) as revenue from 	customer, 	orders, 	lineitem, 	supplier, 	nation, 	region where 	c_custkey = o_custkey 	and l_orderkey = o_orderkey 	and l_suppkey = s_suppkey 	and c_nationkey = s_nationkey 	and s_nationkey = n_nationkey 	and n_regionkey = r_regionkey 	and r_name = \'ASIA\' 	and o_orderdate >= date \'1994-01-01\' 	and o_orderdate < date \'1994-01-01\' + interval \'1\' year group by 	n_name order by 	revenue desc ; '])

        ret_arr.append(['select 	sum(l_extendedprice * l_discount) as revenue from 	lineitem where 	l_shipdate >= date \'1994-01-01\' 	and l_shipdate < date \'1994-01-01\' + interval \'1\' year 	and l_discount between 0.05 and 0.07 	and l_quantity < 24; '])
        #ret_arr.append(['select 	supp_nation, 	cust_nation, 	l_year, 	sum(volume) as revenue from 	( 		select 			n1.n_name as supp_nation, 			n2.n_name as cust_nation, 			extract(year from l_shipdate) as l_year, 			l_extendedprice * (1 - l_discount) as volume 		from 			supplier, 			lineitem, 			orders, 			customer, 			nation n1, 			nation n2 		where 			s_suppkey = l_suppkey 			and o_orderkey = l_orderkey 			and c_custkey = o_custkey 			and s_nationkey = n1.n_nationkey 			and c_nationkey = n2.n_nationkey 			and ( 				(n1.n_name = \'FRANCE\' and n2.n_name = \'GERMANY\') 				or (n1.n_name = \'GERMANY\' and n2.n_name = \'FRANCE\') 			) 			and l_shipdate between date \'1995-01-01\' and date \'1996-12-31\' 	) as shipping group by 	supp_nation, 	cust_nation, 	l_year order by 	supp_nation, 	cust_nation, 	l_year; '])
        #ret_arr.append(['select 	o_year, 	sum(case 		when nation = \'BRAZIL\' then volume 		else 0 	end) / sum(volume) as mkt_share from 	( 		select 			extract(year from o_orderdate) as o_year, 			l_extendedprice * (1 - l_discount) as volume, 			n2.n_name as nation 		from 			part, 			supplier, 			lineitem, 			orders, 			customer, 			nation n1, 			nation n2, 			region 		where 			p_partkey = l_partkey 			and s_suppkey = l_suppkey 			and l_orderkey = o_orderkey 			and o_custkey = c_custkey 			and c_nationkey = n1.n_nationkey 			and n1.n_regionkey = r_regionkey 			and r_name = \'AMERICA\' 			and s_nationkey = n2.n_nationkey 			and o_orderdate between date \'1995-01-01\' and date \'1996-12-31\' 			and p_type = \'ECONOMY ANODIZED STEEL\' 	) as all_nations group by 	o_year order by 	o_year; '])
        #ret_arr.append(['select 	nation, 	o_year, 	sum(amount) as sum_profit from 	( 		select 			n_name as nation, 			extract(year from o_orderdate) as o_year, 			l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount 		from 			part, 			supplier, 			lineitem, 			partsupp, 			orders, 			nation 		where 			s_suppkey = l_suppkey 			and ps_suppkey = l_suppkey 			and ps_partkey = l_partkey 			and p_partkey = l_partkey 			and o_orderkey = l_orderkey 			and s_nationkey = n_nationkey 			and p_name like \'%green%\' 	) as profit group by 	nation, 	o_year order by 	nation, 	o_year desc; '])
        #ret_arr.append(['select 	 	* from 	partsupp limit 1000 ; '])


        ret_arr.append(['select 	ps_partkey, 	sum(ps_supplycost * ps_availqty) as value from 	partsupp, 	supplier, 	nation where 	ps_suppkey = s_suppkey 	and s_nationkey = n_nationkey 	and n_name = \'GERMANY\' group by 	ps_partkey  having 	sum(ps_supplycost * ps_availqty) > 	( 		select 			sum(ps_supplycost * ps_availqty) * 0.000100000000 		from 			partsupp, 			supplier, 			nation 		where 			ps_suppkey = s_suppkey 			and s_nationkey = n_nationkey 			and n_name = \'GERMANY\' 	) order by 	value desc; '])
        ret_arr.append(['select 	l_shipmode, 	sum(case 		when o_orderpriority = \'1-URGENT\' or o_orderpriority = \'2-HIGH\' 		then 1 		else 0 	end) as high_line_count, 	sum(case 		when o_orderpriority <> \'1-URGENT\' or o_orderpriority <> \'2-HIGH\' 		then 1 		else 0 	end) as low_line_count from 	orders, 	lineitem where 	o_orderkey = l_orderkey 	and (l_shipmode = \'MAIL\' or l_shipmode = \'SHIP\') 	and l_commitdate < l_receiptdate 	and l_shipdate < l_commitdate 	and l_receiptdate >= date \'1994-01-01\' 	and l_receiptdate < date \'1994-01-01\' + interval \'1\' year group by 	l_shipmode order by 	l_shipmode ; '])
        #ret_arr.append(['select 	c_count, 	count(*) as custdist from 	( 		select 			c_custkey, 			count(o_orderkey) as c_count 		from 			customer left outer join orders on 				c_custkey = o_custkey 				and o_comment not like \'%special%requests%\' 		group by 			c_custkey 	) as c_orders  group by 	c_count order by 	custdist desc, 	c_count desc; '])
        #ret_arr.append(['select 	100.00 * sum(case 		when p_type like \'PROMO%\' 		then l_extendedprice * (1 - l_discount) 		else 0 	end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue from 	lineitem, 	part where 	l_partkey = p_partkey 	and l_shipdate >= date \'1995-09-01\' 	and l_shipdate < date \'1995-10-01\' ; '])
        #ret_arr.append([' select 	s_suppkey, 	s_name, 	s_address, 	s_phone      from 	supplier where 	s_suppkey < 1000 order by 	s_suppkey; '])

        ret_arr.append(['select 	p_brand, 	p_type, 	p_size, 	count(distinct ps_suppkey) as supplier_cnt from 	partsupp, 	part where 	p_partkey = ps_partkey 	and p_brand <> \'Brand#45\' 	and p_type not like \'MEDIUM POLISHED%\' 	and p_size in (49, 14, 23, 45, 19, 3, 36, 9) 	and ps_suppkey not in ( 		select 			s_suppkey 		from 			supplier 		where 			s_comment like \'%Customer%Complaints%\' 	) group by 	p_brand, 	p_type, 	p_size order by 	supplier_cnt desc, 	p_brand, 	p_type, 	p_size; '])
        ret_arr.append(['select 	sum(l_extendedprice) / 7.0 as avg_yearly from 	lineitem, 	part where 	p_partkey = l_partkey 	and p_brand = \'Brand#23\' 	and p_container = \'MED BOX\' 	and l_quantity < ( 		select 			0.2 * avg(l_quantity) 		from 			lineitem 		where 			l_partkey = p_partkey 	) '])
        #ret_arr.append(['select 	c_name, 	c_custkey, 	o_orderkey, 	o_orderdate, 	o_totalprice, 	sum(l_quantity) from 	customer, 	orders, 	lineitem where 	o_orderkey in ( 		select 			l_orderkey 		from 			lineitem 		group by 			l_orderkey having 				sum(l_quantity) > 300 	) 	and c_custkey = o_custkey 	and o_orderkey = l_orderkey group by 	c_name, 	c_custkey, 	o_orderkey, 	o_orderdate, 	o_totalprice order by 	o_totalprice desc, 	o_orderdate limit 100; '])
        ret_arr.append(['select 	sum(l_extendedprice* (1 - l_discount)) as revenue from 	lineitem, 	part where 	p_partkey = l_partkey 	and (l_shipmode = \'AIR\' or l_shipmode = \'AIR REG\') 	and l_shipinstruct = \'DELIVER IN PERSON\' 	and (( 		p_brand = \'Brand#12\' 		and (p_container = \'SM CASE\' or p_container = \'SM BOX\' or p_container = \'SM PACK\' or p_container = \'SM PKG\') 		and l_quantity >= 1 and l_quantity <= 1 + 10 		and p_size between 1 and 5 	) 	or 	( 		p_brand = \'Brand#23\' 		and (p_container = \'MED BAG\' or p_container = \'MED BOX\' or p_container = \'MED PKG\' or p_container = \'MED PACK\') 		and l_quantity >= 10 and l_quantity <= 10 + 10 		and p_size between 1 and 10 	) 	or 	( 		p_brand = \'Brand#34\' 		and (p_container = \'LG CASE\' or p_container = \'LG BOX\' or p_container = \'LG PACK\' or p_container = \'LG PKG\') 		and l_quantity >= 20 and l_quantity <= 20 + 10 		and p_size between 1 and 15 	)); '])
        #ret_arr.append(['select 	s_name, 	s_address from 	supplier, 	nation where 	s_suppkey in ( 		select 			ps_suppkey 		from 			partsupp 		where 			ps_partkey in ( 				select 					p_partkey 				from 					part 				where 					p_name like \'forest%\' 			) 			and ps_availqty > ( 				select 					0.5 * sum(l_quantity) 				from 					lineitem 				where 					l_partkey = ps_partkey 					and l_suppkey = ps_suppkey 					and l_shipdate >= date \'1994-01-01\' 					and l_shipdate < date \'1994-01-01\' + interval \'1\' year 			) 	) 	and s_nationkey = n_nationkey 	and n_name = \'CANADA\' order by 	s_name; '])

        #ret_arr.append(['select 	s_name, 	count(*) as numwait from 	supplier, 	lineitem l1, 	orders, 	nation where 	s_suppkey = l1.l_suppkey 	and o_orderkey = l1.l_orderkey 	and o_orderstatus = \'F\' 	and l1.l_receiptdate > l1.l_commitdate 	and exists ( 		select 			* 		from 			lineitem l2 		where 			l2.l_orderkey = l1.l_orderkey 			and l2.l_suppkey <> l1.l_suppkey 	) 	and not exists ( 		select 			* 		from 			lineitem l3 		where 			l3.l_orderkey = l1.l_orderkey 			and l3.l_suppkey <> l1.l_suppkey 			and l3.l_receiptdate > l3.l_commitdate 	) 	and s_nationkey = n_nationkey 	and n_name = \'SAUDI ARABIA\' group by 	s_name order by 	numwait desc, 	s_name limit 100; '])
        #ret_arr.append(['select 	cntrycode, 	count(*) as numcust, 	sum(c_acctbal) as totacctbal from 	( 		select 			substring(c_phone from 1 for 2) as cntrycode, 			c_acctbal 		from 			customer 		where 			substring(c_phone from 1 for 2) in 				(\'13\', \'31\', \'23\', \'29\', \'30\', \'18\', \'17\') 			and c_acctbal > ( 				select 					avg(c_acctbal) 				from 					customer 				where 					c_acctbal > 0.00 					and substring(c_phone from 1 for 2) in 						(\'13\', \'31\', \'23\', \'29\', \'30\', \'18\', \'17\') 			) 			and not exists ( 				select 					* 				from 					orders 				where 					o_custkey = c_custkey 			) 	) as custsale group by 	cntrycode order by 	cntrycode; '])




        return ret_arr

    def generateLPQueries(self):
        ret_arr = []
        ret_arr.append(['select * from part '])
        ret_arr.append(['select * supplier where s_region = \'AMERICA\' '])
        ret_arr.append(['select * supplier where s_nation = \'UNITED STATES\' '])

        return ret_arr

    def populateQueryTable(self):
        str = self.generateQueriesNonDiscretized()
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
