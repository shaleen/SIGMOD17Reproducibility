__author__ = 'shaleen'
import random

pricing_functions_possible = ['bucketEntropy', 'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',

                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                              ]

table_choosing_policy_possible = ['chooseTableInProportion', 'chooseTableRandomly', 'chooseFixed']

pricing_functions = ['disagreementCount', 'TsallisEntropy', 'bucketEntropy',  'disagreementEntropyCount',
                     'disagreementCountRandom', 'TsallisEntropyRandom', 'bucketEntropyRandom',  'disagreementEntropyCountRandom'
                    #'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice',
                     #'queryHistoryLP', 'disagreementCountHistory', 'weightedDisagreementCountHistory'
                     ]

per_pricing_function_per_table_policy={}

for i in range(0, len(pricing_functions_possible)):
    per_pricing_function_per_table_policy[pricing_functions_possible[i]]={}

support_count = [10]
table_choosing_policy = 'chooseFixed'

db_price = {}
db_price['Country'] = 33.33
db_price['City'] = 33.33
db_price['CountryLanguage'] = 33.33

def combinedPrice():
    ret_value = 0
    for key, value in db_price.items():
        ret_value += value
    return float(ret_value)

update_changes_per_table = {}
update_changes_per_table['Country'] = 0
update_changes_per_table['City'] = 0
update_changes_per_table['CountryLanguage'] = 0

def resetUpdateChangesPerTable():
    update_changes_per_table['Country'] = 0
    update_changes_per_table['City'] = 0
    update_changes_per_table['CountryLanguage'] = 0

def chooseTableRandomly():
    rand_int = random.randint(0,2);
    return rand_int

def chooseFixed():
    return 0

def chooseTableInProportion():
    r = random.uniform(0, 1)
    s = 0
    l = [(0, db_price['Country']/combinedPrice()), (1, db_price['City']/combinedPrice()), (2, db_price['CountryLanguage']/combinedPrice())]
    for item, prob in l:
        s += prob
        if s >= r:
            return item
    return item

update_sequence_by_table = [] #used by support set to encode each support set element is an update of which table