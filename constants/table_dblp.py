# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random

c = [0.6, 0.1, 0.25, 1]

pk_values={}
table_fields={}
table_fields['dblp'] = ['FromNodeId','ToNodeId']

table_fields_weight={}
table_fields_weight['dblp'] = [(0, 0.5), (1, 0.5)]

field_choosing_policy_possible = ['chooseFieldInProportion','chooseFieldRandomly']
field_choosing_policy = 'chooseFieldRandomly'


def chooseFieldRandomly(table_name):
    rand_int = random.randint(0, len(pk_values[table_name]) - 1)
    return rand_int

def chooseFieldInProportion(table_name):
    r = random.uniform(0, 1)
    s = 0
    l = table_fields_weight[table_name]
    for item, prob in l:
        s += prob
        if s >= r:
            return item
    return item


pk_values['dblp'] = [[x] for x in range (1, 1049867)]

pk_names={}
pk_names['dblp'] = ['id']

pk_type={}
pk_type['dblp'] = ['Integer']

support_fields={}
support_fields['dblp'] = ['FromNodeId','ToNodeId']

def getFromNodeId(val=None):
    if val == None:
        return str(random.randint(1, 425875))
    else:
        return str(val)

def getToNodeId(val=None):
    if val == None:
        return str(random.randint(1, 425956))
    else:
        return str(val)


in_domain = {}
in_domain['dblp'] = {}
in_domain['dblp']['FromNodeId'] = getFromNodeId
in_domain['dblp']['ToNodeId'] = getToNodeId


table_price = {}
table_price['Email'] = 100



