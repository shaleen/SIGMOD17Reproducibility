__author__ = 'shaleen'
import random

pricing_functions_possible = ['bucketEntropy', 'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',
                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                              ]

table_choosing_policy_possible = ['chooseTableInProportion', 'chooseTableRandomly', 'chooseFixed']

pricing_functions = ['bucketEntropy','disagreementCount', 'disagreementCountWeight'
                    #'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',
                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                     ]

per_pricing_function_per_table_policy={}

for i in range(0, len(pricing_functions_possible)):
    per_pricing_function_per_table_policy[pricing_functions_possible[i]]={}

support_count = [1000]
table_choosing_policy = 'chooseFixed'

db_price = {}
db_price['customer'] = 25
db_price['supplier'] = 25
db_price['part'] = 25
db_price['lineorder'] = 25
db_price['dwdate'] = 0

def combinedPrice():
    ret_value = 0
    for key, value in db_price.items():
        ret_value += value
    return float(ret_value)

update_changes_per_table = {}
update_changes_per_table['customer'] = 0
update_changes_per_table['supplier'] = 0
update_changes_per_table['part'] = 0
update_changes_per_table['lineorder'] = 0
update_changes_per_table['dwdate'] = 0

def resetUpdateChangesPerTable():
    update_changes_per_table['customer'] = 0
    update_changes_per_table['supplier'] = 0
    update_changes_per_table['part'] = 0
    update_changes_per_table['lineorder'] = 0
    update_changes_per_table['dwdate'] = 0

def chooseTableRandomly():
    rand_int = random.randint(0,3);
    return rand_int

def chooseFixed():
    return 3

def chooseTableInProportion():
    r = random.uniform(0, 1)
    s = 0
    l = [(0, db_price['country']/combinedPrice()), (1, db_price['supplier']/combinedPrice()), (2, db_price['part']/combinedPrice()),
         (3, db_price['dwdate']/combinedPrice()), (4, db_price['lineorder']/combinedPrice())]
    for item, prob in l:
        s += prob
        if s >= r:
            return item
    return item

update_sequence_by_table = [] #used by support set to encode each support set element is an update of which table