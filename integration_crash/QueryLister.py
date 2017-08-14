__author__ = 'shaleen'

from integration_crash import dbutils

class Query:

    def generateQueries(self):

        ret_arr = []


        return ret_arr


    def generateQueriesNonDiscretized(self):

        ret_arr = []

        ret_arr.append(['select state, count(*) from crash group by State;'])
        ret_arr.append(['select count(*) from crash where State = \'Texas\' and Gender = \'Male\' and Alcohol_Results > 0.0'])
        ret_arr.append(['select sum(Fatalities_in_crash) from crash where State = \'California\' and Crash_Date >= date \'2011-01-01\' and Crash_Date < date \'2011-01-01\' + interval \'6\' month;'])
        ret_arr.append(['select count(Fatalities_in_crash) from crash where State = \'Wisconsin\' and Injury_Severity = \'Fatal Injury (K)\' and (Atmospheric_Condition = \'Snow\');'])


        return ret_arr

    def generateLPQueries(self):
        ret_arr = []
        ret_arr.append(['select * from part '])
        ret_arr.append(['select * supplier where s_region = \'AMERICA\' '])
        ret_arr.append(['select * supplier where s_nation = \'UNITED STATES\' '])

        return ret_arr

    def populateQueryTable(self):
        str = self.generateQueriesNonDiscretized()
        dbutils.DBUtils.cursor.execute('delete from Queries')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('ALTER TABLE Queries AUTO_INCREMENT = 1')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('update Queries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `Queries`(`query`) VALUES (%s)', str)

    def populateLPQueryTable(self):
        str = self.generateLPQueries()
        dbutils.DBUtils.cursor.execute('delete from LPQueries')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('ALTER TABLE LPQueries AUTO_INCREMENT = 1')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.nextset()
        dbutils.DBUtils.cursor.execute('update LPQueries set checksum_base = \'\', checksum_support = \'\'')
        dbutils.DBUtils.cursor.fetchall()
        dbutils.DBUtils.cursor.executemany('INSERT INTO `LPQueries`(`query`) VALUES (%s)', str)


if __name__ == "__main__":

    q = Query()
    q.populateQueryTable()
