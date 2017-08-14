# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
import FieldPolicy
from constants import table_tpch
from integration_tpch import dbutils
from constants import pricing_tpch
import sys
import copy
import re
from timeit import default_timer
class Generator:

    policy = FieldPolicy.Policy()

    def generateSupportSet(self, table_names, count, newtablenames=False):
        pricing_tpch.resetUpdateChangesPerTable()
        pricing_tpch.update_sequence_by_table = []
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        support_set_pk = []
        for i in range(1, count):
            m = getattr(pricing_tpch, pricing_tpch.table_choosing_policy)
            rand_int = m()
            if rand_int == 0:
                complete_result = self.policy.generateRandomUpdateCell('lineitem',
                                                                        table_tpch.support_fields['lineitem'][random.randint(0,len(table_tpch.support_fields['lineitem']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['lineitem'] += 1
                pricing_tpch.update_sequence_by_table.append('lineitem')
            if rand_int == 1:
                complete_result = self.policy.generateRandomUpdateCell('orders',
                                                                        table_tpch.support_fields['orders'][random.randint(0,len(table_tpch.support_fields['orders']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['orders'] += 1
                pricing_tpch.update_sequence_by_table.append('orders')
            if rand_int == 2:
                complete_result = self.policy.generateRandomUpdateCell('partsupp',
                                                                        table_tpch.support_fields['partsupp'][random.randint(0,len(table_tpch.support_fields['partsupp']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['partsupp'] += 1
                pricing_tpch.update_sequence_by_table.append('partsupp')
            if rand_int == 3:
                complete_result = self.policy.generateRandomUpdateCell('customer',
                                                                        table_tpch.support_fields['customer'][random.randint(0,len(table_tpch.support_fields['customer']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['customer'] += 1
                pricing_tpch.update_sequence_by_table.append('customer')
            if rand_int == 4:
                complete_result = self.policy.generateRandomUpdateCell('supplier',
                                                                        table_tpch.support_fields['supplier'][random.randint(0,len(table_tpch.support_fields['supplier']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['supplier'] += 1
                pricing_tpch.update_sequence_by_table.append('supplier')
            if rand_int == 5:
                complete_result = self.policy.generateRandomUpdateCell('nation',
                                                                        table_tpch.support_fields['nation'][random.randint(0,len(table_tpch.support_fields['nation']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['nation'] += 1
                pricing_tpch.update_sequence_by_table.append('nation')
            if rand_int == 6:
                complete_result = self.policy.generateRandomUpdateCell('region',
                                                                        table_tpch.support_fields['region'][random.randint(0,len(table_tpch.support_fields['region']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['region'] += 1
                pricing_tpch.update_sequence_by_table.append('region')
            if rand_int == 7:
                complete_result = self.policy.generateRandomUpdateCell('part',
                                                                        table_tpch.support_fields['part'][random.randint(0,len(table_tpch.support_fields['part']) - 1)],
                                                                        1, 0.5, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                support_set_pk += complete_result[4]
                pricing_tpch.update_changes_per_table['part'] += 1
                pricing_tpch.update_sequence_by_table.append('part')

        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value, support_set_pk]


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


if __name__ == "__main__":
    print sys.stdout.encoding
    g = Generator()
    #g.generateSupportSet(None, 1000)
    g.insertIntoDB(1000)
