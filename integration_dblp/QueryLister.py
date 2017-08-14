__author__ = 'shaleen'

from integration_dblp import dbutils

class Query:


    def generateQueriesNonDiscretized(self):

        ret_arr = []

        ret_arr.append(['select FromNodeId, count(ToNodeId) from dblp group by FromNodeId having count(ToNodeId) > 100;'])
        ret_arr.append(['select avg(cnt) from (select FromNodeId, count(ToNodeId) as cnt from dblp group by FromNodeId ) as rc;'])
        ret_arr.append(['select count(*) from dblp A where FromNodeId > 10000;'])
        ret_arr.append(['select FromNodeId, count(*) from dblp A where A.FromNodeId in (select FromNodeId from dblp B where B.ToNodeId = 38868) group by FromNodeId;'])
        ret_arr.append(['select ToNodeId from dblp where (FromNodeId = 148255 or FromNodeId = 45479);'])
        ret_arr.append(['select FromNodeId, count(*) as collab from dblp group by ToNodeId having collab = 1;'])
        ret_arr.append(['select * from dblp A where A.FromNodeId = 38868 or A.ToNodeId = 38868;'])

        return ret_arr

    def generateLPQueries(self):
        ret_arr = []
        ret_arr.append(['select * from Country '])
        ret_arr.append(['select * from Country where Continent=\'Europe\' and Population > 5000000 '])
        ret_arr.append(['select CountryCode, sum(Population) from City group by CountryCode '])

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
