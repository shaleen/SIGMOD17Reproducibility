# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
from integration_ssb import dbutils
from constants import table_ssb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Policy:

    updateindup = False

    def generateRandomUpdateCell(self, table_name, field_name, count, p_1, p_2, counter, newtablenames=False):
        if random.random() <= p_1:
            return self.swapField(table_name, field_name, count, counter, newtablenames)
        else:
            if random.random() <= p_2:
                return self.cellRandomWithinDomain(table_name, field_name, count, counter, newtablenames)
            else:
                return self.cellRandomOutsideDomain(table_name, field_name, count, counter, newtablenames)

    def executeQuery(self, query):
        dbutils.DBUtils.cursor.execute(query)
        res = dbutils.DBUtils.cursor.fetchall()
        return res[0][0]

    def cellRandomOutsideDomain(self, table_name, field_name, count, counter):
        support_set = []
        support_set_undo_value = []
        for i in range(0, count):
            ret_res = True
            while (ret_res):
                index_1 = random.randint(0, len(table_ssb.pk_values[table_name]) - 1)
                val = table_ssb.pk_values[table_name][index_1]
                string_1 = 'UPDATE ' + table_name + '_view' + ' SET ' + field_name + ' = ' + \
                           table_ssb.in_domain[table_name][field_name]()
                query_for_actual = 'select ' + field_name + ' from ' + table_name + \
                                   ' where ' + self.getWhereCondition(table_name, val)
                print query_for_actual
                #val_1 = self.executeQuery(query_for_actual)
                ret_res = False#self.checkIfDuplicateCell(table_name, field_name, val, [val_1])
            support_set.append([string_1, i + counter])

        print support_set
        return support_set


    def cellRandomWithinDomain(self, table_name, field_name, count, counter, newtablenames):
        support_set = []
        support_set_value = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_pk = []
        if newtablenames:
            print_tn = table_name+'Duplicate'
        else:
            if self.updateindup == True:
                print_tn = table_name+'Duplicate_view'
            else:
                print_tn = table_name+'_view'
        for i in range(0, count):
            ret_res = True
            while (ret_res):
                print "Inside cellrandom"
                index_1 = getattr(table_ssb, table_ssb.field_choosing_policy)(table_name)
                val = table_ssb.pk_values[table_name][index_1]
                where_cond = self.getWhereCondition(table_name, val)
                query_for_actual_1 = 'select ' + field_name + ' from ' + table_name + ' where ' + where_cond
                res_1 = self.executeQuery(query_for_actual_1)
                print query_for_actual_1
                res_1 = table_ssb.in_domain[table_name][field_name](res_1)
                res_random = table_ssb.in_domain[table_name][field_name]()
                string_1 = 'UPDATE ' + print_tn + ' SET ' + field_name + ' = ' \
                           + res_random + ' WHERE ' + where_cond
                string_1_undo = 'UPDATE ' + print_tn + ' SET ' + field_name + ' = ' \
                           + '(' + query_for_actual_1 + ')' + ' WHERE ' + where_cond

                val_1 = self.executeQuery(query_for_actual_1)
                print res_random, " compared to ", res_1
                print "normal query : ", string_1
                print "undo query : ", string_1_undo
                if res_random == res_1:
                    ret_res = True
                else:
                    ret_res = False
                print "Going out"
            support_set.append([string_1, i + counter])
            support_set_value.append(res_random)
            support_set_undo.append([string_1_undo, i + counter])
            support_set_undo_value.append(val_1)
            support_set_pk.append(val)
        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value, support_set_pk]

    def quotedString(self, table_name, value, index):
        if table_ssb.pk_type[table_name][index] == 'String':
            return "'"+str(value)+"'"
        return str(value)

    def getWhereCondition(self, table_name, val):
        ret_str = table_ssb.pk_names[table_name][0] + ' = ' + self.quotedString(table_name, val[0], 0)
        for i in range(1, len(val)):
            ret_str = ret_str +  ' AND ' + table_ssb.pk_names[table_name][i] + ' = ' + self.quotedString(table_name, val[i], i)
        return ret_str

    def getSelectCondition(self, fields):
        ret_str = fields[0]
        for i in range(1, len(fields)):
            ret_str = ret_str + ',' +fields[i]
        return ret_str

    def swapField(self, table_name, field_name, count, counter, newtablesnames):
        if table_ssb.multiple_conditions_for_swap == False:
            return self.swapFieldSingleSet(table_name, field_name, count, counter, newtablesnames)
        else:
            return self.swapFieldMultipleSet(table_name, field_name, count, counter, newtablesnames)

    def swapFieldSingleSet(self, table_name, field_name, count, counter, newtablenames=False):
        #ignore whatever field is sent
        support_set = []
        support_set_value = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_pk = []
        if newtablenames:
            print_tn = table_name+'Duplicate'
        else:
            if self.updateindup == True:
                print_tn = table_name+'Duplicate_view'
            else:
                print_tn = table_name+'_view'
        for i in range(0, count):
            ret_res = True
            while(ret_res):
                index_1 = getattr(table_ssb, table_ssb.field_choosing_policy)(table_name)
                index_2 = getattr(table_ssb, table_ssb.field_choosing_policy)(table_name)
                val_1 = table_ssb.pk_values[table_name][index_1]
                val_2 = table_ssb.pk_values[table_name][index_2]
                if index_1 == index_2:
                    continue
                where_cond_1 = self.getWhereCondition(table_name, val_1)
                where_cond_2 = self.getWhereCondition(table_name, val_2)
                string_1 = 'UPDATE ' + print_tn
                string_2 = 'UPDATE ' + print_tn
                string_1_undo = 'UPDATE ' + print_tn
                string_2_undo = 'UPDATE ' + print_tn
                query_for_actual_1 = 'select ' + field_name + ' from ' + table_name + ' where ' + where_cond_1
                print query_for_actual_1
                res_1 = self.executeQuery(query_for_actual_1)
                query_for_actual_2 = 'select ' + field_name + ' from ' + table_name + ' where ' + where_cond_2
                print query_for_actual_2
                res_2 = self.executeQuery(query_for_actual_2)
                print res_1, " compared to ", res_2
                if res_1 == res_2:
                    ret_res = True
                else:
                    ret_res = False
                str_1 = table_ssb.in_domain[table_name][field_name](res_1)
                str_2 = table_ssb.in_domain[table_name][field_name](res_2)
                print str_1, " compared with ", str_2
                string_1 += ' SET ' + field_name + ' =  ' + str_2
                string_2 += ' SET ' + field_name + ' =  ' + str_1
                string_1_undo += ' SET ' + field_name + ' = (' + query_for_actual_1 + ')'
                string_2_undo += ' SET ' + field_name + ' = (' + query_for_actual_2 + ')'
                string_1 += ' where ' + where_cond_1
                string_2 += ' where ' + where_cond_2
                string_1_undo += ' WHERE ' + where_cond_1
                string_2_undo += ' WHERE ' + where_cond_2
            support_set.append([string_1, i + counter])
            support_set.append([string_2, i + counter])
            support_set_undo.append(([string_1_undo, i + counter]))
            support_set_undo.append(([string_2_undo, i + counter]))
            support_set_value.append(res_2)
            support_set_value.append(res_1)
            support_set_undo_value.append(res_1)
            support_set_undo_value.append(res_2)
            support_set_pk.append(val_1)
            support_set_pk.append(val_2)
        print support_set
        print support_set_undo
        return [support_set, support_set_undo, support_set_undo_value, support_set_value, support_set_pk]


    def swapFieldMultipleSet(self, table_name, field_name, count, counter):
        #ignore whatever field is sent
        support_set = []
        support_set_value = []
        support_set_undo = []
        support_set_undo_value = []
        randint = random.randint(1, len(table_ssb.support_fields[table_name]))
        fields = random.sample(range(0, len(table_ssb.support_fields[table_name])), randint)
        print fields
        string_1 = 'UPDATE ' + table_name + '_view SET '
        string_2 = 'UPDATE ' + table_name + '_view SET '
        string_1_undo = 'UPDATE ' + table_name + '_view SET '
        string_2_undo = 'UPDATE ' + table_name + '_view SET '
        change_index = False
        for i in range(0, count):
            while(True):
                index_1 = getattr(table_ssb, table_ssb.field_choosing_policy)(table_name)
                index_2 = getattr(table_ssb, table_ssb.field_choosing_policy)(table_name)
                val_1 = table_ssb.pk_values[table_name][index_1]
                val_2 = table_ssb.pk_values[table_name][index_2]
                if index_1 == index_2:
                    continue
                where_cond_1 = self.getWhereCondition(table_name, val_1)
                where_cond_2 = self.getWhereCondition(table_name, val_2)
                for j in range(0, len(fields)):
                    change_index = False
                    field_name = table_ssb.support_fields[table_name][fields[j]]
                    while (True):
                        query_for_actual_1 = 'select ' + field_name + ' from ' + table_name + ' where ' + where_cond_1
                        print query_for_actual_1
                        res_1 = self.executeQuery(query_for_actual_1)
                        query_for_actual_2 = 'select ' + field_name + ' from ' + table_name + ' where ' + where_cond_2
                        print query_for_actual_2
                        res_2 = self.executeQuery(query_for_actual_2)
                        print res_1, " compared to ", res_2
                        if res_1 == res_2:
                            change_index = True
                            break
                        str_1 = table_ssb.in_domain[table_name][field_name](res_1)
                        str_2 = table_ssb.in_domain[table_name][field_name](res_2)
                        print str_1, " compared with ", str_2
                        string_1 += field_name + ' =  ' + str_2
                        string_2 += field_name + ' =  ' + str_1
                        string_1_undo += field_name + ' = (' + query_for_actual_1 + ')'
                        string_2_undo += field_name + ' = (' + query_for_actual_2 + ')'
                        if j != len(fields) - 1:
                            string_1 += ', '
                            string_2 += ', '
                        break
                    if change_index == True:
                        break
                if change_index == True:
                    continue
                else:
                    break
            string_1 += ' WHERE ' + where_cond_1
            string_2 += ' WHERE ' + where_cond_2
            string_1_undo += ' WHERE ' + where_cond_1
            string_2_undo += ' WHERE ' + where_cond_2
            support_set.append([string_1, i + counter])
            support_set.append([string_2, i + counter])
            support_set_undo.append(([string_1_undo, i + counter]))
            support_set_undo.append(([string_2_undo, i + counter]))
        print support_set
        print support_set_undo
        return [support_set, support_set_undo, support_set_undo_value, support_set_value]


if __name__ == "__main__":
    print "test"
