# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
import FieldPolicy
from constants import table_dblp
from integration_dblp import dbutils
from constants import pricing_dblp
import sys
import copy
class Generator:

    policy = FieldPolicy.Policy()

    def generateSupportSet(self, table_names, count, newtablenames=False):
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        for i in range(1, count):
            complete_result = self.policy.generateRandomUpdateCell('dblp',
                                                                    table_dblp.support_fields['dblp'][random.randint(0,len(table_dblp.support_fields['dblp']) - 1)],
                                                                    1, 0.5, 1, i, newtablenames)
            support_set += complete_result[0]
            support_set_undo += complete_result[1]
            support_set_undo_value += complete_result[2]
            support_set_value += complete_result[3]

        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value]


    def ringDatabase(self, table_name, count):
        support_set_do_undo = self.generateSupportSet(None, count)
        ret_arr_result = []
        ret_arr_result += support_set_do_undo[0]
        support_set_undo = copy.deepcopy(support_set_do_undo[1])
        random.shuffle(support_set_undo)
        for i in range(0, len(support_set_undo)):
            support_set_undo[i][1] = i + 1 + len(support_set_do_undo[0])

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
    g.generateSupportSet(None, 10)
    #g.insertIntoDB(100)
