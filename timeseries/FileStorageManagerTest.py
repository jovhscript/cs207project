import unittest
import os
from series import *
from interfaces import *
from FileStorageManager import CreateDB

### INSTRUCTION:
### run the following line to get the coverage of the test
### py.test --doctest-modules  --cov --cov-report term-missing CreateDB.py test_CreateDB.py

class DBTest(unittest.TestCase):

    ### Setup the test database
    def setUp(self):
        self.testDB = CreateDB('testDB.dbdb', cachesize=3)
        self.testDB_noCache = CreateDB('testDB_nocache.dbdb', cachesize=0)
        self.ts = TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5])
        self.ts1 = TimeSeries([0, 1, 3.5, 5, 8], times=[0.5, 1, 2, 3, 10.5])
        self.ts2 = TimeSeries([1, 1.5, 5], times=None)
        self.ts3 = TimeSeries([20], times=[4])
        self.ts4 = TimeSeries([])

    ### Remove the test database after done
    def tearDown(self):
        os.remove('testDB.dbdb')
        os.remove('testDB_nocache.dbdb')
        del self.testDB
        del self.testDB_noCache
        del self.ts
        del self.ts2
        del self.ts3

    ### Test store, get and size
    ### Note that when testing "store", "get" is also tested, for the general cases. More edge cases are covered later.
    ### 1. has id
    def test_withID(self):
        ### with string id
        self.testDB.store_ts(id="aaa", ts=self.ts)
        self.assertEquals(self.testDB.get_ts("aaa"), TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5]))
        self.assertEquals(self.testDB.get_size("aaa"), 5)
        ### with integer id
        self.testDB.store_ts(id=1, ts=self.ts)
        self.assertEquals(self.testDB.get_ts(1), TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5]))
        self.assertEquals(self.testDB.get_size(1), 5)

    ### 2. has no id
    def test_withNoID(self):
        id_gen = self.testDB.store_ts(ts=self.ts)
        self.assertEquals(self.testDB.get_ts(id_gen), TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5]))
        self.assertEquals(self.testDB.get_size(id_gen), 5)

    ### 3. has no time
    def test_withNoTime(self):
        self.testDB.store_ts(id=1, ts=self.ts2)
        ts_retrieved = self.testDB.get_ts(1)
        self.assertEquals(self.testDB.get_ts(1), TimeSeries([1, 1.5, 5], times=None))
        self.assertEquals(self.testDB.get_size(1), 3)

    ### 4. duplicate id
    def test_IDAlreadyInDB(self):
        self.testDB.store_ts(id=1, ts=self.ts)
        self.testDB.store_ts(id=1, ts=self.ts1)
        self.assertEquals(self.testDB.get_ts(1), self.ts1)

    ### 5. empty timeseries
    def test_emptyTimeseries(self):
        self.testDB.store_ts(id=1, ts=self.ts4)
        self.assertEquals(self.testDB.get_size(1), 0)

    ### 6. ts is not timeseries
    def test_inputNotTimeseries(self):
        with self.assertRaises(TypeError):
            self.testDB.store_ts(ts=["aaa", 1, 5])

    ### test caching
    def test_cache(self):
        self.testDB.store_ts(id=1, ts=self.ts)
        self.testDB.store_ts(id=2, ts=self.ts1)
        self.testDB.store_ts(id=3, ts=self.ts2)
        self.testDB.store_ts(id=4, ts=self.ts3)

        # No cache except lastStored, which points to {4, ts3}
        self.assertEquals(self.testDB.cache_mostAccessed, {})
        self.assertEquals(self.testDB.cache_lastAccessed, {})
        self.assertEquals(self.testDB.cache_lastStored, {'4': self.ts3})

        # First get
        self.testDB.get_ts(id=1)
        self.assertEquals(self.testDB.cache_mostAccessed, {'1': self.ts})
        self.assertEquals(self.testDB.cache_lastAccessed, {'1': self.ts})
        self.assertEquals(self.testDB.count_accessed, {'1': 1})

        # Next few gets
        self.testDB.get_ts(1)
        self.testDB.get_ts(1)
        self.testDB.get_ts(2)
        self.testDB.get_ts(2)
        self.assertEquals(self.testDB.cache_mostAccessed, {'1': self.ts, '2': self.ts1})
        self.assertEquals(self.testDB.cache_lastAccessed, {'2': self.ts1})
        self.assertEquals(self.testDB.count_accessed, {'1': 3, '2': 2})

        # After cache is full
        self.testDB.get_ts(3)
        self.testDB.get_ts(4)
        self.testDB.get_ts(4)
        self.assertEquals(self.testDB.cache_mostAccessed, {'1': self.ts, '2': self.ts1, '4': self.ts3})
        self.assertEquals(self.testDB.cache_lastAccessed, {'4': self.ts3})
        self.assertEquals(self.testDB.count_accessed, {'1': 3, '2': 2, '3': 1, '4': 2})
#
# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.makeSuite(DBTest))
#     return suite
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner(failfast=True)
#     runner.run(suite())