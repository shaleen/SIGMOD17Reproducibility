# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
from integration_tpch import dbutils

c = [0.6, 0.1, 0.25, 1]

pk_values={}
table_fields={}

table_fields['lineitem'] = ['l_orderkey','l_partkey','l_suppkey','l_linenumber','l_quantity','l_extendedprice','l_discount','l_tax','l_returnflag','l_linestatus','l_shipdate','l_commitdate','l_receiptdate','l_shipinstruct','l_shipmode','l_comment']
table_fields['orders'] = ['o_orderkey','o_custkey','o_orderstatus','o_totalprice','o_orderdate','o_orderpriority','o_clerk','o_shippriority',
                         'o_comment']
table_fields['customer'] = ['c_custkey','c_name','c_address','c_nationkey','c_phone','c_acctbal','c_mktsegment','c_comment']
table_fields['partsupp'] = ['ps_partkey','ps_suppkey','ps_availqty','ps_supplycost','ps_comment']
table_fields['part'] = ['p_partkey', 'p_name', 'p_mfgr', 'p_brand', 'p_type','p_size', 'p_container', 'p_retailprice', 'p_comment']
table_fields['supplier'] = ['s_suppkey', 's_name', 's_address', 's_nationkey', 's_phone', 's_acctbal', 's_comment']
table_fields['nation'] = ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment']
table_fields['region'] = ['r_regionkey', 'r_name', 'r_comment']


field_choosing_policy_possible = ['chooseFieldInProportion','chooseFieldRandomly']
field_choosing_policy = 'chooseFieldRandomly'
multiple_conditions_for_swap = False

def chooseFieldRandomly(table_name):
    rand_int = random.randint(0, len(pk_values[table_name]) - 1)
    return rand_int

dbutils.DBUtils.cursor.execute('select o_orderkey from orders;')
res = dbutils.DBUtils.cursor.fetchall()
o_ok = []
for i in range(0, len(res)):
    o_ok.append(res[i][0])
pk_values['customer'] = [[x] for x in range(1, 150001)]
pk_values['supplier'] = [[x] for x in range(1, 10001)]
pk_values['part'] = [[x] for x in range (1, 200001)]
pk_values['partsupp'] = [[x] for x in range (1, 800001)]
pk_values['nation'] = [[x] for x in range (0, 25)]
pk_values['region'] = [[x] for x in range (0, 5)]
pk_values['lineitem'] = [[x] for x in range(1, 6001216)]
pk_values['orders'] = [[o_ok[i]] for i in range(0, len(o_ok)) ]


pk_names={}
pk_names['customer'] = ['c_custkey']
pk_names['supplier'] = ['s_suppkey']
pk_names['part'] = ['p_partkey']
pk_names['partsupp'] = ['ps_id']
pk_names['region'] = ['r_regionkey']
pk_names['nation'] = ['n_nationkey']
pk_names['lineitem'] = ['l_id']
pk_names['orders'] = ['o_orderkey']

pk_type={}
pk_type['customer'] = ['Integer']
pk_type['supplier'] = ['Integer']
pk_type['part'] = ['Integer']
pk_type['partsupp'] = ['Integer']
pk_type['region'] = ['Integer']
pk_type['nation'] = ['Integer']
pk_type['lineitem'] = ['Integer']
pk_type['orders'] = ['Integer']

support_fields={}
support_fields['customer'] = ['c_name','c_nationkey','c_acctbal','c_mktsegment']
support_fields['supplier'] = ['s_name', 's_nationkey', 's_acctbal']
support_fields['part'] = ['p_mfgr', 'p_brand', 'p_type','p_size', 'p_container', 'p_retailprice']
support_fields['partsupp'] = ['ps_availqty','ps_supplycost']
support_fields['region'] = ['r_name']
support_fields['nation'] = ['n_name', 'n_regionkey']
support_fields['lineitem'] = ['l_partkey','l_suppkey','l_quantity','l_extendedprice','l_returnflag','l_linestatus','l_shipdate','l_commitdate','l_receiptdate','l_shipinstruct','l_shipmode']
support_fields['orders'] = ['o_custkey','o_orderstatus','o_totalprice','o_orderdate','o_orderpriority','o_clerk']

in_domain={}

def gets_name(val='test'):
    field = ['Supplier#0000'+str(x).rjust(5, '0') for x in range(1, 10001)]
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''

def gets_nationkey(val='test'):
    field = [x for x in range(0,25)]
    if val == 'test':
        return str(field[random.randint(0, len(field) - 1)])
    else:
        return str(val)


def gets_acctbal(val='test'):
    if val == 'test':
        return str(random.randint(-998, 10000))
    else:
        return str(val)

in_domain['supplier'] = {}
in_domain['supplier']['s_name'] = gets_name
in_domain['supplier']['s_nationkey'] = gets_nationkey
in_domain['supplier']['s_acctbal'] = gets_acctbal

c_field = ['Customer#000'+str(x).rjust(6, '0') for x in range(1, 150001)]
def getc_name(val='test'):
    if val == 'test' or val == None:
        return '\'' + c_field[random.randint(0, len(c_field) - 1)] + '\''
    else:
        return '\'' + val + '\''

def getc_acctbal(val='test'):
    if val == 'test':
        return str(random.randint(-1000, 10000))
    else:
        return str(val)

def getc_mktsegment(val='test'):
    field = ['BUILDING','AUTOMOBILE','MACHINERY','HOUSEHOLD','FURNITURE']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''


in_domain['customer'] = {}
in_domain['customer']['c_name'] = getc_name
in_domain['customer']['c_nationkey'] = gets_nationkey
in_domain['customer']['c_mktsegment'] = getc_mktsegment
in_domain['customer']['c_acctbal'] = getc_acctbal


dbutils.DBUtils.cursor.execute('select distinct(p_name) from part')
res = dbutils.DBUtils.cursor.fetchall()
p_name = []
for i in range(0, len(res)):
    p_name.append(res[i][0])

def getp_name(val='test'):
    if val == 'test':
        return '\''+p_name[random.randint(0, len(p_name) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getp_mfgr(val='test'):
    field = ['Manufacturer#1','Manufacturer#2','Manufacturer#3','Manufacturer#4','Manufacturer#5']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''



def getp_brand(val='test'):
    field = ['Brand#11','Brand#12','Brand#13','Brand#14','Brand#15','Brand#21','Brand#22','Brand#23','Brand#24','Brand#25','Brand#31','Brand#32','Brand#33','Brand#34','Brand#35','Brand#41','Brand#42','Brand#43','Brand#44','Brand#45','Brand#51','Brand#52','Brand#53','Brand#54','Brand#55',]
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getp_type(val='test'):
    field = ['PROMO BURNISHED COPPER','LARGE BRUSHED BRASS','STANDARD POLISHED BRASS','SMALL PLATED BRASS','STANDARD POLISHED TIN','PROMO PLATED STEEL','SMALL PLATED COPPER','PROMO BURNISHED TIN','SMALL BURNISHED STEEL','LARGE BURNISHED STEEL','STANDARD BURNISHED NICKEL','MEDIUM ANODIZED STEEL','MEDIUM BURNISHED NICKEL','SMALL POLISHED STEEL','LARGE ANODIZED BRASS','PROMO PLATED TIN','ECONOMY BRUSHED STEEL','SMALL ANODIZED NICKEL','LARGE POLISHED NICKEL','SMALL BURNISHED TIN','PROMO POLISHED BRASS','MEDIUM BURNISHED TIN','MEDIUM PLATED STEEL','STANDARD BRUSHED COPPER','SMALL BRUSHED STEEL','LARGE ANODIZED TIN','PROMO PLATED COPPER','PROMO ANODIZED TIN','STANDARD BRUSHED TIN','ECONOMY PLATED BRASS','ECONOMY PLATED NICKEL','LARGE BRUSHED STEEL','MEDIUM ANODIZED BRASS','SMALL BURNISHED COPPER','LARGE POLISHED TIN','ECONOMY ANODIZED BRASS','SMALL POLISHED TIN','ECONOMY BURNISHED COPPER','ECONOMY ANODIZED TIN','PROMO POLISHED STEEL','MEDIUM PLATED TIN','SMALL BRUSHED NICKEL','LARGE BURNISHED BRASS','STANDARD BRUSHED STEEL','ECONOMY BURNISHED NICKEL','STANDARD BURNISHED TIN','LARGE BURNISHED COPPER','ECONOMY BRUSHED COPPER','MEDIUM BURNISHED BRASS','MEDIUM POLISHED TIN','LARGE POLISHED COPPER','SMALL BURNISHED NICKEL','STANDARD BRUSHED BRASS','MEDIUM BRUSHED COPPER','PROMO ANODIZED NICKEL','SMALL BRUSHED TIN','PROMO ANODIZED STEEL','MEDIUM POLISHED BRASS','STANDARD PLATED BRASS','STANDARD ANODIZED TIN','SMALL BRUSHED COPPER','ECONOMY POLISHED STEEL','PROMO ANODIZED BRASS','PROMO PLATED BRASS','ECONOMY BRUSHED TIN','ECONOMY POLISHED TIN','PROMO BURNISHED NICKEL','STANDARD PLATED TIN','LARGE PLATED STEEL','STANDARD BURNISHED STEEL','LARGE BRUSHED TIN','STANDARD ANODIZED BRASS','LARGE ANODIZED STEEL','MEDIUM PLATED BRASS','SMALL POLISHED COPPER','PROMO PLATED NICKEL','STANDARD BURNISHED COPPER','LARGE BRUSHED COPPER','PROMO BRUSHED STEEL','PROMO POLISHED TIN','MEDIUM POLISHED NICKEL','STANDARD POLISHED STEEL','PROMO POLISHED NICKEL','LARGE POLISHED STEEL','MEDIUM ANODIZED TIN','MEDIUM BRUSHED NICKEL','SMALL PLATED NICKEL','STANDARD BURNISHED BRASS','MEDIUM BURNISHED STEEL','SMALL PLATED STEEL','ECONOMY PLATED STEEL','MEDIUM BRUSHED STEEL','STANDARD PLATED STEEL','STANDARD ANODIZED STEEL','ECONOMY PLATED TIN','SMALL ANODIZED TIN','PROMO BRUSHED COPPER','MEDIUM PLATED COPPER','LARGE PLATED BRASS','MEDIUM POLISHED STEEL','SMALL POLISHED NICKEL','ECONOMY ANODIZED STEEL','MEDIUM BURNISHED COPPER','SMALL ANODIZED BRASS','STANDARD POLISHED COPPER','MEDIUM ANODIZED COPPER','ECONOMY BURNISHED TIN','SMALL ANODIZED STEEL','MEDIUM BRUSHED BRASS','LARGE BURNISHED NICKEL','ECONOMY BURNISHED BRASS','STANDARD BRUSHED NICKEL','SMALL ANODIZED COPPER','PROMO BRUSHED NICKEL','LARGE ANODIZED NICKEL','STANDARD PLATED COPPER','LARGE PLATED COPPER','MEDIUM ANODIZED NICKEL','PROMO BRUSHED BRASS','MEDIUM PLATED NICKEL','STANDARD POLISHED NICKEL','LARGE BURNISHED TIN','LARGE PLATED NICKEL','PROMO BURNISHED BRASS','ECONOMY POLISHED COPPER','STANDARD ANODIZED COPPER','SMALL BURNISHED BRASS','LARGE POLISHED BRASS','ECONOMY ANODIZED NICKEL','SMALL PLATED TIN','ECONOMY BRUSHED NICKEL','PROMO BURNISHED STEEL','PROMO BRUSHED TIN','MEDIUM BRUSHED TIN','PROMO POLISHED COPPER','STANDARD ANODIZED NICKEL','ECONOMY POLISHED NICKEL','LARGE BRUSHED NICKEL','ECONOMY BURNISHED STEEL','SMALL POLISHED BRASS','ECONOMY ANODIZED COPPER','STANDARD PLATED NICKEL','LARGE ANODIZED COPPER','ECONOMY POLISHED BRASS','SMALL BRUSHED BRASS','PROMO ANODIZED COPPER','LARGE PLATED TIN','ECONOMY BRUSHED BRASS','MEDIUM POLISHED COPPER','ECONOMY PLATED COPPER']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getp_size(val='test'):
    if val == 'test':
        return str(random.randint(1, 50))
    else:
        return str(val)

def getp_retailprice(val='test'):
    if val == 'test':
        return str(random.randint(901, 2099))
    else:
        return str(val)

def getp_container(val='test'):
    field = ['JUMBO PKG','LG CASE','WRAP CASE','MED DRUM','SM PKG','MED BAG','SM BAG','LG DRUM','LG CAN','WRAP BOX','JUMBO CASE','JUMBO PACK','JUMBO BOX','MED PACK','LG BOX','JUMBO JAR','MED CASE','JUMBO BAG','SM CASE','MED PKG','LG BAG','LG PKG','JUMBO CAN','SM JAR','WRAP JAR','SM PACK','WRAP BAG','WRAP PKG','WRAP DRUM','LG PACK','MED CAN','SM BOX','LG JAR','SM CAN','WRAP PACK','MED JAR','WRAP CAN','SM DRUM','MED BOX','JUMBO DRUM']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

in_domain['part'] = {}
in_domain['part']['p_name'] = getp_name
in_domain['part']['p_mfgr'] = getp_mfgr
in_domain['part']['p_brand'] = getp_brand
in_domain['part']['p_retailprice'] = getp_retailprice
in_domain['part']['p_size'] = getp_size
in_domain['part']['p_type'] = getp_type
in_domain['part']['p_container'] = getp_container

def getr_name(val='test'):
    field = ['AFRICA','AMERICA','ASIA','EUROPE','MIDDLE EAST']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''


in_domain['region'] = {}
in_domain['region']['r_name'] = getr_name


def getn_name(val='test'):
    field = ['ALGERIA','ARGENTINA','BRAZIL','CANADA','EGYPT','ETHIOPIA','FRANCE','GERMANY','INDIA','INDONESIA','IRAN','IRAQ','JAPAN','JORDAN','KENYA','MOROCCO','MOZAMBIQUE','PERU','CHINA','ROMANIA','SAUDI ARABIA','VIETNAM','RUSSIA','UNITED KINGDOM','UNITED STATES',]
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''


def getn_regionkey(val='test'):
    if val == 'test':
        return str(random.randint(0, 4))
    else:
        return str(val)

in_domain['nation'] = {}
in_domain['nation']['n_name'] = getn_name
in_domain['nation']['n_regionkey'] = getn_regionkey

def getps_availqty(val='test'):
    if val == 'test':
        return str(random.randint(1, 9999))
    else:
        return str(val)

def getps_supplycost(val='test'):
    if val == 'test':
        return str(random.randint(1, 1000))
    else:
        return str(val)
in_domain['partsupp'] = {}
in_domain['partsupp']['ps_availqty'] = getps_availqty
in_domain['partsupp']['ps_supplycost'] = getps_supplycost



def getl_partkey(val='test'):

    if val == 'test':
        return str(pk_values['part'][random.randint(0, len(pk_values['part']) - 1)][0])
    else:
        return str(val)

dbutils.DBUtils.cursor.execute('select distinct(l_commitdate) from lineitem;')
res = dbutils.DBUtils.cursor.fetchall()
date_c = []
for i in range(0, len(res)):
    date_c.append(str(res[i][0]))

def getl_commitdate(val='test'):
    if val == 'test':
        return '\''+date_c[random.randint(0, len(date_c) - 1)] +'\''
    else:
        return '\'' + str(val) + '\''

dbutils.DBUtils.cursor.execute('select distinct(l_receiptdate) from lineitem;')
res = dbutils.DBUtils.cursor.fetchall()
date_r = []
for i in range(0, len(res)):
    date_r.append(str(res[i][0]))

def getl_receiptdate(val='test'):
    if val == 'test':
        return '\''+date_r[random.randint(0, len(date_r) - 1)] +'\''
    else:
        return '\'' + str(val) + '\''

dbutils.DBUtils.cursor.execute('select distinct(l_shipdate) from lineitem;')
res = dbutils.DBUtils.cursor.fetchall()
date_s = []
for i in range(0, len(res)):
    date_s.append(str(res[i][0]))

def getl_shipdate(val='test'):
    if val == 'test':
        return '\''+date_s[random.randint(0, len(date_s) - 1)] +'\''
    else:
        return '\'' + str(val) + '\''

def getl_shipmode(val='test'):
    field=['TRUCK','MAIL','REG AIR','AIR','FOB','RAIL','SHIP']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''


def getl_shipinstruct(val='test'):
    field=['DELIVER IN PERSON','TAKE BACK RETURN','NONE''COLLECT COD']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getl_linestatus(val='test'):
    field=['O','F']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getl_returnflag(val='test'):
    field=['N','R','A']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def getl_suppkey(val='test'):

    if val == 'test':
        return str(pk_values['supplier'][random.randint(0, len(pk_values['supplier']) - 1)][0])
    else:
        return str(val)

def getl_quantity(val='test'):
    if val == 'test':
        return str(random.randint(1,50))
    else:
        return str(val)

def getl_extendedprice(val='test'):
    if val == 'test':
        return str(random.randint(901,104950))
    else:
        return str(val)

def getl_tax(val='test'):
    if val == 'test':
        return str(random.randint(0,100))
    else:
        return str(val)

def getl_discount(val='test'):
    if val == 'test':
        return str(random.randint(0,100))
    else:
        return str(val)

in_domain['lineitem'] = {}
in_domain['lineitem']['l_partkey'] = getl_partkey
in_domain['lineitem']['l_suppkey'] = getl_suppkey
in_domain['lineitem']['l_quantity'] = getl_quantity
in_domain['lineitem']['l_extendedprice'] = getl_extendedprice
in_domain['lineitem']['l_discount'] = getl_discount
in_domain['lineitem']['l_tax'] = getl_tax
in_domain['lineitem']['l_returnflag'] = getl_returnflag
in_domain['lineitem']['l_linestatus'] = getl_linestatus
in_domain['lineitem']['l_shipdate'] = getl_shipdate
in_domain['lineitem']['l_commitdate'] = getl_commitdate
in_domain['lineitem']['l_receiptdate'] = getl_receiptdate
in_domain['lineitem']['l_shipinstruct'] = getl_shipinstruct
in_domain['lineitem']['l_shipmode'] = getl_shipmode
in_domain['lineitem']['l_'] = getl_discount


def geto_custkey(val='test'):
    if val == 'test':
        return str(pk_values['customer'][random.randint(0, len(pk_values['customer']) - 1)][0])
    else:
        return str(val)

def geto_orderstatus(val='test'):
    field=['O','F','P']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

def geto_totalprice(val='test'):
    if val == 'test':
        return str(random.randint(858,555285))
    else:
        return str(val)

dbutils.DBUtils.cursor.execute('select distinct(o_orderdate) from orders;')
res = dbutils.DBUtils.cursor.fetchall()
date_order = []
for i in range(0, len(res)):
    date_order.append(str(res[i][0]))

def geto_orderdate(val='test'):
    if val == 'test':
        return '\''+date_order[random.randint(0, len(date_order) - 1)] +'\''
    else:
        return '\'' + str(val) + '\''

def geto_orderpriority(val='test'):
    field=['5-LOW','1-URGENT','4-NOT SPECIFIED','2-HIGH','3-MEDIUM']
    if val == 'test':
        return '\''+field[random.randint(0, len(field) - 1)] +'\''
    else:
        return '\'' + val + '\''

dbutils.DBUtils.cursor.execute('select distinct(o_clerk) from orders;')
res = dbutils.DBUtils.cursor.fetchall()
clerk_order = []
for i in range(0, len(res)):
    clerk_order.append(res[i][0])

def geto_clerk(val='test'):
    if val == 'test':
        return '\''+clerk_order[random.randint(0, len(clerk_order) - 1)] +'\''
    else:
        return '\'' + val + '\''

in_domain['orders'] = {}
in_domain['orders']['o_custkey'] = geto_custkey
in_domain['orders']['o_orderdate'] = geto_orderdate
in_domain['orders']['o_orderstatus'] = geto_orderstatus
in_domain['orders']['o_clerk'] = geto_clerk
in_domain['orders']['o_totalprice'] = geto_totalprice
in_domain['orders']['o_orderpriority'] = geto_orderpriority

table_price = {}
table_price['customer'] = 25
table_price['supplier'] = 25
table_price['partsupp'] = 25
table_price['lineitem'] = 25




