__author__ = 'shaleen'
from pricingfunction import Utils
from utility import dbutils
from constants import pricing_country
from constants import table_country
import math
import cvxpy as cvx
import numpy as np
import pickle
from timeit import default_timer

weightarr = []

#with open('weights9999.txt','rb') as f:
#        weightarr = pickle.load(f)


def disagreementCount(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            count += data[j][i]
        y_plot.append(float(count)*100/support_count)
    return y_plot

def disagreementCountWeight(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            count += data[j][i]*weightarr[j]
        y_plot.append(float(count)*100/support_count)
    return y_plot

def disagreementEntropyCount(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            count += data[j][i]
        if count == 0:
            count = 1
        y_plot.append(float(math.log(count,2))*100/math.log(support_count,2))
    return y_plot

def disagreementCountHistory(data=None,  no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    global_count = 0
    per_view_consistent = [1 for i in range(support_count)]
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            if data[j][i] == 1 and per_view_consistent[j] == 1:
                count += data[j][i]
                per_view_consistent[j] = 0
        global_count += count
        y_plot.append(float(global_count)*100/support_count)
    return y_plot

def weightedDisagreementCount(data=None,  no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            db_str = pricing_country.update_sequence_by_table[j]
            count += (data[j][i]*(float(pricing_country.db_price[db_str])/pricing_country.update_changes_per_table[db_str]))
        y_plot.append(float(count) * 100/pricing_country.combinedPrice())
    return y_plot

def weightedDisagreementCountHistory(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    y_plot = []
    global_count = 0
    per_view_consistent = [1 for i in range(support_count)]
    for i in range(1, no_of_queries + 1):
        count = 0
        for j in range(0, support_count):
            if data[j][i] == 1 and per_view_consistent[j] == 1:
                per_view_consistent[j] = 0
                db_str = pricing_country.update_sequence_by_table[j]
                count += (data[j][i]*(float(pricing_country.db_price[db_str])/pricing_country.update_changes_per_table[db_str]))
        global_count += count
        y_plot.append(float(global_count) * 100/pricing_country.combinedPrice())
    return y_plot

def bucketEntropy():
    no_of_queries = dbutils.DBUtils.no_of_queries()
    support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    y_plot = []
    for i in range(1, no_of_queries+1):
        dict = {}
        dbutils.DBUtils.cursor.execute('select checksum_support, checksum_base from Queries where idQueries = '+str(i))
        res = dbutils.DBUtils.cursor.fetchall()
        for r in res:
            ret_str = r[0][1:]
            support_size = ret_str.split(';')
            for ii in range(0, support_count):
                if support_size[ii] not in dict:
                    dict[support_size[ii]] = 1
                else:
                    dict[support_size[ii]] += 1
            total = 0
            entropy = 0
            for key, value in dict.iteritems():
                entropy += (value*math.log(value, 2))
                total += value

            y_plot.append((1 - entropy/(support_count*math.log(support_count,2)))*100)
    return y_plot

def TsallisEntropy():
    q = 2
    no_of_queries = dbutils.DBUtils.no_of_queries()
    support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    y_plot = []
    for i in range(1, no_of_queries+1):
        dict = {}
        dbutils.DBUtils.cursor.execute('select checksum_support, checksum_base from Queries where idQueries = '+str(i))
        res = dbutils.DBUtils.cursor.fetchall()
        for r in res:
            ret_str = r[0][1:]
            support_size = ret_str.split(';')
            for ii in range(0, support_count):
                if support_size[ii] not in dict:
                    dict[support_size[ii]] = 1
                else:
                    dict[support_size[ii]] += 1
            total = 0
            entropy = 0
            for key, value in dict.iteritems():
                entropy += (value*value)
                total += value

            y_plot.append((1 - float(entropy)/(support_count*support_count))*100)
    return y_plot

def findWeightsLP(data=None):
    no_of_queries_lp = dbutils.DBUtils.no_of_queries_lp()
    support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    if data==None:
        data = Utils.PricerUtils.disagreementMatrixLP(dbutils.DBUtils.cursor, no_of_queries_lp, support_count)
    for i in range(0, support_count):
        data[i][0] = 1
    inp = np.asarray(data)
    inp = np.delete(inp, 0, 1)
    x = cvx.Variable(1, support_count+1)
    A = inp
    c = np.asarray([table_country.c])
    obj = cvx.Maximize(cvx.sum_entries(cvx.entr(x)))
    constraints = [x*A == c]
    prob = cvx.Problem(obj, constraints)
    prob.solve(solver=cvx.SCS, verbose=True, max_iters=10000)
    if prob.status == cvx.INFEASIBLE:
        return None
    weights = []
    for i in np.nditer(x.value,flags=['refs_ok']):
        weights.append(i*100)
    print "size - ", x.size
    with open('weights9999.txt','wb') as f:
        pickle.dump(weights, f)
    return weights

def findWeightsLPAndPrice():
    no_of_queries = dbutils.DBUtils.no_of_queries()
    support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    weights = findWeightsLP()
    if weights == None:
        return []
    data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    price_arr = []
    for i in range(1, no_of_queries + 1):
        price = 0
        for j in range(0, support_count):
            if data[j][i] == 1:
                price += weights[j]
        price_arr.append(price*100)
    return price_arr

def queryHistoryLP(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    weights = findWeightsLP()
    if weights == None:
        return []
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    per_view_consistent = [1 for i in range(support_count)]
    y_plot = []
    price = 0
    for i in range(1, no_of_queries + 1):
        per_query_price = 0
        for j in range(0, support_count):
            if data[j][i] == 1 and per_view_consistent[j] == 1:
                per_view_consistent[j] = 0
                per_query_price += weights[j]
        price += per_query_price
        y_plot.append(price*100)
    return y_plot


def queryHistory(data=None, no_of_queries=None, support_count=None):
    if no_of_queries == None:
        no_of_queries = dbutils.DBUtils.no_of_queries()
    if support_count == None:
        support_count = dbutils.DBUtils.no_of_elements_in_support_set()
    # weights = findWeightsLP()
    # if weights == None:
    #     return []
    if data == None:
        data = Utils.PricerUtils.disagreementMatrix(dbutils.DBUtils.cursor, no_of_queries, support_count)
    per_view_consistent = [1 for i in range(support_count)]
    y_plot = []
    price = 0
    for i in range(1, no_of_queries + 1):
        start = default_timer()
        per_query_price = 0
        for j in range(0, support_count):
            if data[j][i] == 1 and per_view_consistent[j] == 1:
                per_view_consistent[j] = 0
                per_query_price += weightarr[j]
        price += per_query_price
        end = default_timer() - start
        print "Query ",i, " time - ",end
        y_plot.append(price/100)
    return y_plot













