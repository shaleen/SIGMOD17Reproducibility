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

support_count = [5000]
table_choosing_policy = 'chooseFixed'

db_price = {}
db_price['crash'] = 100

def combinedPrice():
    ret_value = 0
    for key, value in db_price.items():
        ret_value += value
    return float(ret_value)

update_changes_per_table = {}
update_changes_per_table['crash'] = 0

def resetUpdateChangesPerTable():
    update_changes_per_table['crash'] = 0

def chooseTableRandomly():
    rand_int = random.randint(0,8);
    return rand_int

def chooseFixed():
    return 0

update_sequence_by_table = []