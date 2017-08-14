__author__ = 'shaleen'
import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from integration_dblp import dbutils
from constants import pricing_dblp
from integration_dblp import Pricer
from supportsetgeneratordblp import Generator
from integration_dblp import QueryLister
from timeit import default_timer
import pickle

class Combiner:

    d = dbutils.DBUtils()
    g = Generator.Generator()
    q = QueryLister.Query()

    def executeProc(self, query_start, query_end, restore_countryview, use_which_query, clean_lpqueries=False):
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        if clean_lpqueries == True:
            dbutils.DBUtils.cursor.execute('update LPQueries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.execute('call restoreDBLPView()')
        start = default_timer()
        stri = "call ExecuteQueries(" + str(query_start) + ", " + str(query_end) + ", " \
                                       + str(self.d.no_of_elements_in_support_set()) + ", " + str(restore_countryview) + ", " + str(use_which_query) +")"
        print stri
        dbutils.DBUtils.cursor.execute(stri)
        dbutils.DBUtils.cursor.fetchall()

        end = default_timer() - start
        print "time : ", end


    def endToEndProcessing(self, query_start, query_end, restore_countryview, use_which_query, clean_lpqueries=False):
        no_of_queries = self.d.no_of_queries()
        for i in range(0, len(pricing_dblp.support_count)):
            labels = []
            y_plots = []
            self.g.insertIntoDB(pricing_dblp.support_count[i])
            self.executeProc(query_start, query_end, restore_countryview, use_which_query, clean_lpqueries)
            for j in range(0, len(pricing_dblp.pricing_functions)):
                m = getattr(Pricer, pricing_dblp.pricing_functions[j])
                y_plots.append(m())
                labels.append(str(pricing_dblp.pricing_functions[j]))
            #self.c.generateChart(range(1, no_of_queries + 1), y_plots, str(pricing_country.support_count[i]) + 'databases.eps', labels)
        return y_plots

    def endToEndProcessingExecutedProc(self):
        no_of_queries = self.d.no_of_queries()
        for i in range(0, len(pricing_dblp.support_count)):
            labels = []
            y_plots = []
            for j in range(0, len(pricing_dblp.pricing_functions)):
                m = getattr(Pricer, pricing_dblp.pricing_functions[j])
                y_plots.append(m())
                labels.append(str(pricing_dblp.pricing_functions[j]))
            return y_plots

    def convertToString(self, queries):
        str = ''
        for i in range(0, len(queries)):
            str = str +  queries[i][0] + '\n'
        return str

if __name__ == "__main__":

    c = Combiner()
    y_plot = c.endToEndProcessingExecutedProc()
    print "price weighted disagreement - ", y_plot[0]
    print "price entropy - ", y_plot[1]
