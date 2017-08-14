__author__ = 'shaleen'
import MySQLdb
from constants import db

db_conn = MySQLdb.Connect("localhost","root","help2012","graph",charset='utf8',use_unicode=True)
db_conn.autocommit(True)

class DBUtils:

    cursor = db_conn.cursor()
    sql ='SET GLOBAL max_allowed_packet=107374182400;'
    cursor.execute(sql)


    @staticmethod
    def no_of_queries():
        DBUtils.cursor.execute('select count(*) from ' + db.QUERY_TABLE)
        res = DBUtils.cursor.fetchall()
        no_of_queries = res[0][0]
        DBUtils.cursor.nextset()
        return no_of_queries

    @staticmethod
    def no_of_queries_lp():
        DBUtils.cursor.execute('select count(*) from LPQueries')
        res = DBUtils.cursor.fetchall()
        no_of_queries = res[0][0]
        DBUtils.cursor.nextset()
        return no_of_queries

    @staticmethod
    def no_of_elements_in_support_set():
        DBUtils.cursor.execute('select count(distinct batchid) from ' + db.SUPPORT_SET_TABLE)
        res = DBUtils.cursor.fetchall()
        support_count = res[0][0]
        DBUtils.cursor.nextset()
        return support_count

    @staticmethod
    def no_of_queries_duplicate():
        DBUtils.cursor.execute('select count(*) from ' + db.QUERY_TABLE +'Duplicate')
        res = DBUtils.cursor.fetchall()
        no_of_queries = res[0][0]
        DBUtils.cursor.nextset()
        return no_of_queries

    @staticmethod
    def no_of_queries_lp_duplicate():
        DBUtils.cursor.execute('select count(*) from LPQueriesDuplicate')
        res = DBUtils.cursor.fetchall()
        no_of_queries = res[0][0]
        DBUtils.cursor.nextset()
        return no_of_queries

    @staticmethod
    def no_of_elements_in_support_set_duplicate():
        DBUtils.cursor.execute('select count(distinct batchid) from ' + db.SUPPORT_SET_TABLE + 'Duplicate')
        res = DBUtils.cursor.fetchall()
        support_count = res[0][0]
        DBUtils.cursor.nextset()
        return support_count