__author__ = 'shaleen'
import random

pricing_functions_possible = ['bucketEntropy', 'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',
                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                              ]

table_choosing_policy_possible = ['chooseTableInProportion', 'chooseTableRandomly', 'chooseFixed']

pricing_functions = ['bucketEntropy','disagreementCount'
                    #'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',
                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                     ]

per_pricing_function_per_table_policy={}

for i in range(0, len(pricing_functions_possible)):
    per_pricing_function_per_table_policy[pricing_functions_possible[i]]={}

support_count = [100000]
table_choosing_policy = 'chooseTableRandomly'

db_price = {}
db_price['lineitem'] = 25
db_price['orders'] = 25
db_price['partsupp'] = 25
db_price['customer'] = 25
db_price['supplier'] = 0
db_price['part'] = 0
db_price['region'] = 25
db_price['nation'] = 25

def combinedPrice():
    ret_value = 0
    for key, value in db_price.items():
        ret_value += value
    return float(ret_value)

update_changes_per_table = {}
update_changes_per_table['customer'] = 0
update_changes_per_table['supplier'] = 0
update_changes_per_table['part'] = 0
update_changes_per_table['partsupp'] = 0
update_changes_per_table['lineitem'] = 0
update_changes_per_table['orders'] = 0
update_changes_per_table['region'] = 0
update_changes_per_table['nation'] = 0

def resetUpdateChangesPerTable():
    update_changes_per_table['customer'] = 0
    update_changes_per_table['supplier'] = 0
    update_changes_per_table['part'] = 0
    update_changes_per_table['partsupp'] = 0
    update_changes_per_table['lineitem'] = 0
    update_changes_per_table['orders'] = 0
    update_changes_per_table['region'] = 0
    update_changes_per_table['nation'] = 0

def chooseTableRandomly():
    rand_int = random.randint(0,8);
    return rand_int

def chooseFixed():
    return 0

def chooseTableInProportion():
    r = random.uniform(0, 1)
    s = 0
    l = [(0, db_price['lineitem']/combinedPrice()), (1, db_price['orders']/combinedPrice()), (2, db_price['partsupp']/combinedPrice()),
         (3, db_price['customer']/combinedPrice()), (4, db_price['nation']/combinedPrice()), (5, db_price['region']/combinedPrice()),
         (6, db_price['supplier']/combinedPrice())]
    for item, prob in l:
        s += prob
        if s >= r:
            return item
    return item

update_sequence_by_table = []