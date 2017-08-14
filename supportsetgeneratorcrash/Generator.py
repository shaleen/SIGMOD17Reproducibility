# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
import FieldPolicy
from constants import table_crash
from integration_crash import dbutils
from constants import pricing_crash
import sys
import copy
import re
from timeit import default_timer
class Generator:

    policy = FieldPolicy.Policy()

    def generateSupportSet(self, table_names, count, newtablenames=False):
        pricing_crash.resetUpdateChangesPerTable()
        pricing_crash.update_sequence_by_table = []
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        for i in range(1, count):
            m = getattr(pricing_crash, pricing_crash.table_choosing_policy)
            rand_int = m()
            if rand_int == 0:
                complete_result = self.policy.generateRandomUpdateCell('crash',
                                                                        table_crash.support_fields['crash'][random.randint(0,len(table_crash.support_fields['crash']) - 1)],
                                                                        1, 0, 1, i, newtablenames)
                support_set += complete_result[0]
                support_set_undo += complete_result[1]
                support_set_undo_value += complete_result[2]
                support_set_value += complete_result[3]
                pricing_crash.update_changes_per_table['crash'] += 1
                pricing_crash.update_sequence_by_table.append('crash')
        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value]


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
    g = Generator()
    g.insertIntoDB(100)
    #g.generateSupportSet(None, 100)

