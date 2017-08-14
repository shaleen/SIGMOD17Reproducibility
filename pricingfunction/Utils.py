__author__ = 'shaleen'
from utility import dbutils

class PricerUtils:

    @staticmethod
    def agreementMatrix(cursor, no_of_queries, support_count):
        data = [[0 for i in range(no_of_queries+1)] for j in range(support_count+1)]
        for i in range(1, no_of_queries + 1):
            cursor.execute('select checksum_support, checksum_base from Queries where idQueries = ' + str(i))
            res = cursor.fetchall()
            checksum_base = res[0][1]
            for r in res:
                ret_str = r[0][1:]
                support_size = ret_str.split(';')
                for j in range(0, len(support_size)):
                    if support_size[j] == checksum_base:
                        data[j][i] = 1
                    else:
                        data[j][i] = 0
        return data

    @staticmethod
    def disagreementMatrix(cursor, no_of_queries, support_count):
        data = [[0 for i in range(no_of_queries+1)] for j in range(support_count+1)]
        for i in range(1, no_of_queries + 1):
            cursor.execute('select checksum_support, checksum_base from Queries where idQueries = ' + str(i))
            res = cursor.fetchall()
            checksum_base = res[0][1]
            for r in res:
                ret_str = r[0][1:]
                support_size = ret_str.split(';')
                for j in range(0, len(support_size)):
                    if support_size[j] == checksum_base:
                        data[j][i] = 0
                    else:
                        data[j][i] = 1
        return data

    @staticmethod
    def disagreementMatrixLP(cursor, no_of_queries, support_count):
        data = [[0 for i in range(no_of_queries+2)] for j in range(support_count+1)]
        for i in range(1, no_of_queries + 1):
            cursor.execute('select checksum_support, checksum_base from LPQueries where idQueries = ' + str(i))
            res = cursor.fetchall()
            checksum_base = res[0][1]
            for r in res:
                ret_str = r[0][1:]
                support_size = ret_str.split(';')
                for j in range(0, len(support_size)):
                    if support_size[j] == checksum_base:
                        data[j][i] = 0
                    else:
                        data[j][i] = 1
        for j in range(0, len(support_size)):
            data[j][no_of_queries+1] = 1
        return data


if __name__ == "__main__":

    PricerUtils.disagreementMatrixLP(dbutils.DBUtils.cursor, dbutils.DBUtils.no_of_queries(), dbutils.DBUtils.no_of_elements_in_support_set())

