__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from integration_crash import dbutils
from constants import pricing_crash
from integration_crash import Pricer
from supportsetgeneratorcrash import Generator
from integration_crash import QueryLister
from timeit import default_timer

class Combiner:

    # support set for DB implementation is supportset250

    d = dbutils.DBUtils()
    g = Generator.Generator()
    q = QueryLister.Query()



    def executeProc(self, query_start, query_end, restore_countryview, use_which_query, clean_lpqueries=False):
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        if clean_lpqueries == True:
            dbutils.DBUtils.cursor.execute('update LPQueries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call restoreCrashView()')
        start = default_timer()
        stri = "call ExecuteQueriesCrash(" + str(query_start) + ", " + str(query_end) + ", " \
                                       + str(self.d.no_of_elements_in_support_set()) + ", " + str(restore_countryview) + ", " + str(use_which_query) +")"
        print stri
        dbutils.DBUtils.cursor.execute(stri)
        dbutils.DBUtils.cursor.fetchall()

        end = default_timer() - start
        print "time : ", end


    def endToEndProcessing(self, query_start, query_end, restore_countryview, use_which_query, clean_lpqueries=False):
        no_of_queries = self.d.no_of_queries()
        for i in range(0, 1):
            labels = []
            y_plots = []
            self.executeProc(query_start, query_end, restore_countryview, use_which_query, clean_lpqueries)
            for j in range(0, len(pricing_crash.pricing_functions)):
                m = getattr(Pricer, pricing_crash.pricing_functions[j])
                y_plots.append(m())
                labels.append(str(pricing_crash.pricing_functions[j]))
        return y_plots

    def endToEndProcessingExecutedProc(self):
        no_of_queries = self.d.no_of_queries()
        for i in range(0, 1):
            labels = []
            y_plots = []
            for j in range(0, len(pricing_crash.pricing_functions)):
                m = getattr(Pricer, pricing_crash.pricing_functions[j])
                y_plots.append(m())
                labels.append(str(pricing_crash.pricing_functions[j]))
        return y_plots

    def convertToString(self, queries):
        str = ''
        for i in range(0, len(queries)):
            str = str +  queries[i][0] + '\n'
        return str

    def insertIntoDB(self, count):
        # self.g.insertIntoDB(count);
        # with open('supportset4999.txt', 'wb') as f:
        #     pickle.dump(support_set, f)
        # with open('supportset9999.txt', 'rb') as f:
        #     support_set = pickle.load(f)
        support_set = None
        self.g.insertIntoDB(count);
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call clearUpdateQuery()')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[0])
        dbutils.DBUtils.cursor.executemany('INSERT INTO `UndoUpdateQuery`(`query`,`batchid`) VALUES (%s,%s)', support_set[1])
        dbutils.DBUtils.cursor.fetchall()
        return support_set

if __name__ == "__main__":
    c = Combiner()
    y_plot = c.endToEndProcessingExecutedProc()
    print "price weighted disagreement - ", y_plot[0]
    print "price entropy - ", y_plot[1]