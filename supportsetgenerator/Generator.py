# -*- coding: utf8 -*-
__author__ = 'shaleen'
import random
import FieldPolicy
from constants import table_country
from integration import dbutils
from constants import pricing_country
import sys
import copy
class Generator:

    policy = FieldPolicy.Policy()

    def generateSupportSet(self, table_names, count, newtablenames=False):
        pricing_country.resetUpdateChangesPerTable()
        pricing_country.update_sequence_by_table = []
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        support_set_pk = []
        for i in range(1, count):
            for j in range(0, random.randint(1,1)):
                m = getattr(pricing_country, pricing_country.table_choosing_policy)
                rand_int = m()
                if rand_int == 0:
                    complete_result = self.policy.generateRandomUpdateCell('Country',
                                                                            table_country.support_fields['Country'][random.randint(0,len(table_country.support_fields['Country']) - 1)],
                                                                            1, 0.25, 1, i, newtablenames)
                    support_set += complete_result[0]
                    support_set_undo += complete_result[1]
                    support_set_undo_value += complete_result[2]
                    support_set_value += complete_result[3]
                    support_set_pk += complete_result[4]
                    pricing_country.update_changes_per_table['Country'] += 1
                    pricing_country.update_sequence_by_table.append('Country')
                if rand_int == 1:
                    complete_result = self.policy.generateRandomUpdateCell('City',
                                                                            table_country.support_fields['City'][random.randint(0,len(table_country.support_fields['City']) - 1)],
                                                                            1, 0, 1, i, newtablenames)
                    support_set += complete_result[0]
                    support_set_undo += complete_result[1]
                    support_set_undo_value += complete_result[2]
                    support_set_value += complete_result[3]
                    support_set_pk += complete_result[4]
                    pricing_country.update_changes_per_table['City'] += 1
                    pricing_country.update_sequence_by_table.append('City')
                if rand_int == 2:
                    complete_result = self.policy.generateRandomUpdateCell('CountryLanguage',
                                                                            table_country.support_fields['CountryLanguage'][random.randint(0,len(table_country.support_fields['CountryLanguage']) - 1)],
                                                                            1, 0, 1, i, newtablenames)
                    support_set += complete_result[0]
                    support_set_undo += complete_result[1]
                    support_set_undo_value += complete_result[2]
                    support_set_value += complete_result[3]
                    support_set_pk += complete_result[4]
                    pricing_country.update_changes_per_table['CountryLanguage'] += 1
                    pricing_country.update_sequence_by_table.append('CountryLanguage')
        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value]



    def generateSupportSetCity(self, table_names, count, newtablenames=False):
        pricing_country.resetUpdateChangesPerTable()
        pricing_country.update_sequence_by_table = []
        support_set = []
        support_set_undo = []
        support_set_undo_value = []
        support_set_value = []
        for i in range(1, count):
            complete_result = self.policy.generateRandomUpdateCell('City',
                                                                    table_country.support_fields['City'][random.randint(0,len(table_country.support_fields['City']) - 1)],
                                                                    1, 0.5, 1, i, newtablenames)
            support_set += complete_result[0]
            support_set_undo += complete_result[1]
            support_set_undo_value += complete_result[2]
            support_set_value += complete_result[3]
            pricing_country.update_changes_per_table['City'] += 1
            pricing_country.update_sequence_by_table.append('City')
        print support_set
        return [support_set, support_set_undo, support_set_undo_value, support_set_value]



    def ringDatabase(self, table_name, count):
        support_set_do_undo = self.generateSupportSet(None, count)
        ret_arr_result = []
        ret_arr_result += support_set_do_undo[0]
        support_set_undo = copy.deepcopy(support_set_do_undo[1])
        random.shuffle(support_set_undo)
        for i in range(0, len(support_set_undo)):
            support_set_undo[i][1] = i + 1 + support_set_do_undo[0][len(support_set_do_undo[0])-1][1]
            if 'Country_view' in support_set_undo[i][0]:
                pricing_country.update_changes_per_table['Country'] += 1
                pricing_country.update_sequence_by_table.append('Country')
            if 'City_view' in support_set_undo[i][0]:
                pricing_country.update_changes_per_table['City'] += 1
                pricing_country.update_sequence_by_table.append('City')
            if 'CountryLanguage_view' in support_set_undo[i][0]:
                pricing_country.update_changes_per_table['CountryLanguage'] += 1
                pricing_country.update_sequence_by_table.append('CountryLanguage')


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
    s = g.generateSupportSet(None, random.randint(100000), newtablenames=True)[0]
    for i in range(0, len(s)):
        dbutils.DBUtils.cursor.execute(s[i][0])


