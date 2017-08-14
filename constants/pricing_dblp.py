__author__ = 'shaleen'
import random

pricing_functions_possible = ['bucketEntropy', 'disagreementCount', 'weightedDisagreementCount', 'findWeightsLPAndPrice']

pricing_functions = ['bucketEntropy', 'disagreementCount']

per_pricing_function_per_table_policy={}

for i in range(0, len(pricing_functions_possible)):
    per_pricing_function_per_table_policy[pricing_functions_possible[i]]={}

support_count = [100]