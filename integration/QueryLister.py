__author__ = 'shaleen'

from integration import dbutils

class Query:

    def bechmarkqueries(self):
        ret_arr = []
        ret_arr.append(['SELECT Code FROM Country WHERE ID < 80'])
        ret_arr.append(['SELECT Code,Name,Continent,Region FROM COUNTRY'])
        ret_arr.append(['SELECT C.Code FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 80  '])
        ret_arr.append(['SELECT Code,Region,LifeExpectancy FROM Country order by Region'])
        return ret_arr

    def generateQueries(self):

        ret_arr = []

        ret_arr.append(['select count(Name) from Country where Continent = \'Asia\''])
        ret_arr.append(['select count(distinct Continent) from Country '])
        ret_arr.append(['select avg(Population) from Country '])
        ret_arr.append(['select max(Population) from Country '])
        ret_arr.append(['select min(LifeExpectancy) from Country '])
        ret_arr.append(['select count(Name) from Country where Name like \'A%\' '])
        ret_arr.append(['select Region, max(SurfaceArea) from Country group by Region '])
        ret_arr.append(['select Continent, max(Population) from Country group by Continent '])
        ret_arr.append(['select Continent, count(Code) from Country group by Continent '])
        ret_arr.append(['select * from Country ']) #10
        ret_arr.append(['select Name from Country where Name like \'A%\' '])
        ret_arr.append(['select * from Country where Continent=\'Europe\' and Population > 5000000 '])
        ret_arr.append(['select * from Country where Region=\'Caribbean\' '])
        ret_arr.append(['select Name from Country where Region=\'Caribbean\' '])
        ret_arr.append(['select Name from Country where Population between 10000000 and 20000000 ']) #15
        ret_arr.append(['select * from Country where Continent=\'Europe\' limit 2 '])
        ret_arr.append(['SELECT Population FROM Country WHERE Code = \'USA\' '])
        ret_arr.append(['select GovernmentForm from Country '])
        ret_arr.append(['select distinct GovernmentForm from Country '])
        ret_arr.append(['SELECT * FROM City WHERE Population >= \'1000000\' AND CountryCode = \'USA\' ']) # 20
        ret_arr.append(['select distinct Language from CountryLanguage where CountryCode=\'USA\' '])
        ret_arr.append(['select * from CountryLanguage where IsOfficial = \'T\' '])
        ret_arr.append(['select Language, count(CountryCode) from CountryLanguage group by Language ']) #23
        ret_arr.append(['select count(Language) from CountryLanguage where CountryCode = \'USA\'  ']) #24
        ret_arr.append(['select CountryCode, sum(Population) from City group by CountryCode '])
        ret_arr.append(['select CountryCode, count(ID) from City group by CountryCode '])
        ret_arr.append(['select * from City where CountryCode = \'GRC\' '])
        ret_arr.append(['select distinct 1 from City where CountryCode = \'USA\' and Population > 10000000 ']) #28
        ret_arr.append(['SELECT Name FROM Country , CountryLanguage WHERE Code = CountryCode AND Language = \'Greek\' '])
        ret_arr.append(['SELECT C.Name FROM Country C, CountryLanguage L WHERE C.Code = L.CountryCode AND L.Language = \'English\' AND L.Percentage >= 50 '])
        ret_arr.append(['SELECT T.district FROM Country C, City T WHERE C.code = \'USA\' AND C.capital = T.id '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage L WHERE C.Code = L.CountryCode AND L.Language = \'Spanish\' '])
        ret_arr.append(['SELECT Name, Language FROM Country , CountryLanguage WHERE Code = CountryCode '])
        ret_arr.append(['SELECT * FROM Country , CountryLanguage WHERE Code = CountryCode '])
        return ret_arr

    def generateQueriesBenchmark(self):

        ret_arr = []

        # ret_arr.append(['select * from Country where ID < 1'])
        # ret_arr.append(['select * from Country where ID < 2'])
        # ret_arr.append(['select * from Country where ID < 4'])
        # ret_arr.append(['select * from Country where ID < 8'])
        # ret_arr.append(['select * from Country where ID < 16'])
        # ret_arr.append(['select * from Country where ID < 32'])
        # ret_arr.append(['select * from Country where ID < 64'])
        # ret_arr.append(['select * from Country where ID < 128'])
        # ret_arr.append(['select * from Country where ID < 256'])
        #
        # ret_arr.append(['select Name from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy  from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld, GovernmentForm from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld, GovernmentForm, HeadOfState from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld, GovernmentForm, HeadOfState, Capital from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld, GovernmentForm, HeadOfState, Capital, Code2 from Country where ID < 256'])
        # ret_arr.append(['select Name, Continent,Region,SurfaceArea, Population,LifeExpectancy, GNP, GNPOld, GovernmentForm, HeadOfState, Capital, Code2, LocalName from Country where ID < 256'])

        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 0  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 0.0750  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 0.1550  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 0.3125  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 0.625  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 1.25  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 2.5  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 5  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 10  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 20  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 40  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 60  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 80  '])
        ret_arr.append(['SELECT * FROM Country C, CountryLanguage CL WHERE C.Code = CL.CountryCode AND CL.Percentage < 100  '])


        # ret_arr.append(['select Region, avg(LifeExpectancy) from Country group by Region order by Region limit 5'])
        # ret_arr.append(['select Region, avg(LifeExpectancy) from Country group by Region order by Region limit 10'])
        # ret_arr.append(['select Region, avg(LifeExpectancy) from Country group by Region order by Region limit 15'])
        # ret_arr.append(['select Region, avg(LifeExpectancy) from Country group by Region order by Region limit 20'])
        # ret_arr.append(['select Region, avg(LifeExpectancy) from Country group by Region order by Region limit 25'])


        return  ret_arr

    def generateLPQueries(self):
        ret_arr = []
        # ret_arr.append(['select * from Country where Population between 100000 and 500000;'])
        # ret_arr.append(['select * from Country where Population between 1000000 and 5000000;'])
        # ret_arr.append(['select * from Country where Population between 6500000 and 7500000;'])
        # ret_arr.append(['select * from Country where Population between 6700000 and 7100000;'])
        # ret_arr.append(['select * from Country where Population between 100 and 10000;'])
        #ret_arr.append(['select * from Country where Population between 4500000 and 7000000;'])
        #ret_arr.append(['select * from Country where Population between 5500000 and 6750000;'])
        #ret_arr.append(['select * from Country where Population between 2000000 and 9000000;'])
        #ret_arr.append(['select * from Country where Population <150000;'])
        ret_arr.append(['select Region from Country where Population between 100000 and 500000;'])
        ret_arr.append(['select LifeExpectancy,SurfaceArea from Country where Population between 500000 and 1000000;'])
        ret_arr.append(['select HeadOfState,Capital from Country where Population between 1000000 and 10000000;'])
        ret_arr.append(['select Continent,Region,IndepYear from Country where Population between 10000000 and 20000000;'])
        ret_arr.append(['select GNP,LocalName from Country where Population between 20000000 and 50000000;'])
        ret_arr.append(['select Region,SurfaceArea from Country where Population between 50000000 and 60000000;'])
        ret_arr.append(['select Capital,Code2 from Country where Population between 60000000 and 80000000;'])
        ret_arr.append(['select SurfaceArea,Continent,Capital from Country where Population between 80000000 and 90000000;'])
        ret_arr.append(['select * from Country where Population between 90000000 and 100000000;'])
        ret_arr.append(['select * from Country where Population between 100000000 and 200000000;'])
        ret_arr.append(['select GNP,GNPOld from Country where Population between 200000000 and 300000000;'])

        return ret_arr

    def populateQueryTable(self):
        str = self.generateQueriesBenchmark()
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
