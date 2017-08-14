# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
from integration_crash import dbutils

c = [0.6, 0.1, 0.25, 1]

pk_values={}
table_fields={}

table_fields['crash'] = ['Age','Alcohol_Results','Atmospheric_Condition','Crash_Date','Drug_Involvement','Fatalities_in_crash','First_Harmful_Event',
                         'Gender','ID','Injury_Severity','Person_Type','Race','Roadway','State','PK']


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
pk_values['crash'] = [[x] for x in range(1, 71116)]


pk_names={}
pk_names['crash'] = ['ID']

pk_type={}
pk_type['crash'] = ['ID']

support_fields={}
support_fields['crash'] = ['Age','Alcohol_Results','Atmospheric_Condition','Crash_Date','Drug_Involvement','Fatalities_in_crash','First_Harmful_Event',
                         'Gender','Injury_Severity','Person_Type','Race','Roadway','State']

in_domain={}

def getAge(val='test'):
    if val == 'test':
        return str(random.randint(0, 111))
    else:
        return str(val)

def getFatalities_in_crash(val='test'):
    if val == 'test':
        return str(random.randint(1, 15))
    else:
        return str(val)

def getAlcohol_Results(val='test'):
    if val == 'test':
        return str(random.uniform(0, 0.6600000262260437))
    else:
        return str(val)

def getAtmospheric_Condition(val='test'):
    field = ['Clear','Cloudy','Rain','Fog, Smog, Smoke','Snow','Blowing Snow','Sleet, Hail (Freezing Rain or Drizzle)','Not Reported','Blowing Sand, Soil, Dirt','Unknown','Severe Crosswinds','Other','']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''


dbutils.DBUtils.cursor.execute('select distinct(Crash_Date) from crash')
res = dbutils.DBUtils.cursor.fetchall()
p_name = []
for i in range(0, len(res)):
    p_name.append(res[i][0])
def getCrash_Date(val='test'):
    if val == 'test' or val == None:
        return '\'' + str(p_name[random.randint(0, len(p_name) - 1)]) + '\''
    else:
        return '\'' + str(val) + '\''

dbutils.DBUtils.cursor.execute('select distinct(First_Harmful_Event) from crash')
res = dbutils.DBUtils.cursor.fetchall()
c_name = []
for i in range(0, len(res)):
    c_name.append(res[i][0])
def getFirst_Harmful_Event(val='test'):
    if val == 'test' or val == None:
        return '\'' + c_name[random.randint(0, len(c_name) - 1)] + '\''
    else:
        return '\'' + val + '\''

def getDrug_Involvement(val='test'):
    field = ['Yes','No','Not Reported','Unknown','N']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''

def getGender(val='test'):
    field = ['Male','Female','Not Reported','Unknown']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''

def getInjury_Severity(val='test'):
    field = ['Non-incapacitating Evident Injury (B)','Fatal Injury (K)','No Injury (O)','Incapacitating Injury (A)','Possible Injury (C)','Injured, Severity Unknown','Unknown']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''

def getPerson_Type(val='test'):
    field = ['Driver of a Motor Vehicle In-Transport','Passenger of a Motor Vehicle In-Transport','Pedestrian','Bicyclist','Occupant of a Motor Vehicle Not In- Transport','Persons on Personal Conveyances','Persons In/On Buildings','Occupant of a Non-Motor Vehicle Transport Device','Unknown Occupant Type in a Motor Vehicle In- Transport','Unknown','Other Cyclist','']
    if val == 'test' or val == None:
        return '\'' + field[random.randint(0, len(field) - 1)] + '\''
    else:
        return '\'' + val + '\''


dbutils.DBUtils.cursor.execute('select distinct(Race) from crash')
res = dbutils.DBUtils.cursor.fetchall()
r_name = []
for i in range(0, len(res)):
    r_name.append(res[i][0])
def getRace(val='test'):
    if val == 'test' or val == None:
        return '\'' + r_name[random.randint(0, len(r_name) - 1)] + '\''
    else:
        return '\'' + val + '\''


dbutils.DBUtils.cursor.execute('select distinct(Race) from crash')
res = dbutils.DBUtils.cursor.fetchall()
ro_name = []
for i in range(0, len(res)):
    ro_name.append(res[i][0])
def getRoadway(val='test'):
    if val == 'test' or val == None:
        return '\'' + ro_name[random.randint(0, len(ro_name) - 1)] + '\''
    else:
        return '\'' + val + '\''

dbutils.DBUtils.cursor.execute('select distinct(State) from crash')
res = dbutils.DBUtils.cursor.fetchall()
s_name = []
for i in range(0, len(res)):
    s_name.append(res[i][0])
def getState(val='test'):
    if val == 'test' or val == None:
        return '\'' + s_name[random.randint(0, len(s_name) - 1)] + '\''
    else:
        return '\'' + val + '\''

in_domain['crash'] = {}
in_domain['crash']['Age'] = getAge
in_domain['crash']['Alcohol_Results'] = getAlcohol_Results
in_domain['crash']['Atmospheric_Condition'] = getAtmospheric_Condition
in_domain['crash']['Crash_Date'] = getCrash_Date
in_domain['crash']['Drug_Involvement'] = getDrug_Involvement
in_domain['crash']['Fatalities_in_crash'] = getFatalities_in_crash
in_domain['crash']['First_Harmful_Event'] = getFirst_Harmful_Event
in_domain['crash']['Gender'] = getGender
in_domain['crash']['Injury_Severity'] = getInjury_Severity
in_domain['crash']['Person_Type'] = getPerson_Type
in_domain['crash']['Race'] = getRace
in_domain['crash']['Roadway'] = getRoadway
in_domain['crash']['State'] = getState


table_price = {}
table_price['crash'] = 100



