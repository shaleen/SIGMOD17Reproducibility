# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
import FieldPolicy
from constants import table_ssb
from integration_ssb import dbutils
from constants import pricing_ssb
import sys
import copy
class Generator:

    policy = FieldPolicy.Policy()

    def generateSupportSet(self, table_names, count, newtablenames=False):
        pricing_ssb.resetUpdateChangesPerTable()
        pricing_ssb.update_sequence_by_table = []
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        support_set_pk = []
        for i in range(1, count):
            m = getattr(pricing_ssb, pricing_ssb.table_choosing_policy)
            rand_int = m()
            if rand_int == 0:
                complete_result = self.policy.generateRandomUpdateCell('customer',
                                                                        table_ssb.support_fields['customer'][random.randint(0,len(table_ssb.support_fields['customer']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_ssb.update_changes_per_table['customer'] += 1
                pricing_ssb.update_sequence_by_table.append('customer')
            if rand_int == 1:
                complete_result = self.policy.generateRandomUpdateCell('supplier',
                                                                        table_ssb.support_fields['supplier'][random.randint(0,len(table_ssb.support_fields['supplier']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_ssb.update_changes_per_table['supplier'] += 1
                pricing_ssb.update_sequence_by_table.append('supplier')
            if rand_int == 2:
                complete_result = self.policy.generateRandomUpdateCell('part',
                                                                        table_ssb.support_fields['part'][random.randint(0,len(table_ssb.support_fields['part']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_ssb.update_changes_per_table['part'] += 1
                pricing_ssb.update_sequence_by_table.append('part')
            if rand_int == 3:
                complete_result = self.policy.generateRandomUpdateCell('lineorder',
                                                                        table_ssb.support_fields['lineorder'][random.randint(0,len(table_ssb.support_fields['lineorder']) - 1)],
                                                                        1, 0, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_ssb.update_changes_per_table['lineorder'] += 1
                pricing_ssb.update_sequence_by_table.append('lineorder')
            if rand_int == 4:
                complete_result = self.policy.generateRandomUpdateCell('dwdate',
                                                                        table_ssb.support_fields['dwdate'][random.randint(0,len(table_ssb.support_fields['dwdate']) - 1)],
                                                                        1, 0, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                pricing_ssb.update_changes_per_table['dwdate'] += 1
                pricing_ssb.update_sequence_by_table.append('dwdate')

        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value,  support_set_pk]


    def ringDatabase(self, table_name, count):
        support_set_do_undo = self.generateSupportSet(None, count)
        ret_arr_result = []
        ret_arr_result += support_set_do_undo[0]
        support_set_undo = copy.deepcopy(support_set_do_undo[1])
        random.shuffle(support_set_undo)
        for i in range(0, len(support_set_undo)):
            support_set_undo[i][1] = i + 1 + len(support_set_do_undo[0])
            if 'customer' in support_set_undo[i][0]:
                pricing_ssb.update_changes_per_table['customer'] += 1
                pricing_ssb.update_sequence_by_table.append('customer')
            if 'supplier' in support_set_undo[i][0]:
                pricing_ssb.update_changes_per_table['supplier'] += 1
                pricing_ssb.update_sequence_by_table.append('supplier')
            if 'part' in support_set_undo[i][0]:
                pricing_ssb.update_changes_per_table['part'] += 1
                pricing_ssb.update_sequence_by_table.append('part')
            if 'lineorder' in support_set_undo[i][0]:
                pricing_ssb.update_changes_per_table['lineorder'] += 1
                pricing_ssb.update_sequence_by_table.append('lineorder')
            if 'dwdate' in support_set_undo[i][0]:
                pricing_ssb.update_changes_per_table['dwdate'] += 1
                pricing_ssb.update_sequence_by_table.append('dwdate')


        ret_arr_result += support_set_undo
        return [ret_arr_result, support_set_do_undo[1]]


    def insertIntoDBRing(self, count):
        support_set = self.ringDatabase(None, count)
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call clearUpdateQuery()')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[0])
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UndoUpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[1])
        dbutils.DBUtils.cursor.fetchall()


    def insertIntoDB(self, count):
        support_set = self.generateSupportSet(None, count)
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call clearUpdateQuery()')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[0])
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UndoUpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[1])
        dbutils.DBUtils.cursor.fetchall()
        return support_set

    def insertIntoDBDuplicate(self, count):
        support_set = self.generateSupportSet(None, count)
        dbutils.DBUtils.cursor.execute('update QueriesDuplicate set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call clearUpdateQueryDuplicate()')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UpdateQueryDuplicate`(`query`,`batchid`) VALUES (%s,%s)', support_set[0])
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UndoUpdateQueryDuplicate`(`query`,`batchid`) VALUES (%s,%s)', support_set[1])
        dbutils.DBUtils.cursor.fetchall()
        return support_set


if __name__ == "__main__":
    print sys.stdout.encoding
    g = Generator()
    #g.generateSupportSet(None, 1000)
    g.insertIntoDB(100)
