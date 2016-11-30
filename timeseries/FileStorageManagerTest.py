import unittest
import os
from series import *
from interfaces import *
from FileStorageManager import *

class test_FileStorageManager(unittest.TestCase):

    ### Setup the test database
    def setUp(self):
        self.testFSM = FileStorageManager('testFSM.dbdb')
        self.ts = TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5])
        self.ts1 = TimeSeries([0, 1, 3.5, 5, 8], times=[0.5, 1, 2, 3, 10.5])
        self.ts2 = TimeSeries([1, 1.5, 5], times=None)
        self.ts3 = ArrayTimeSeries(times=[0.5, 1, 2, 3, 10.5], values=[-1, 0, 1.5, 4, 100])
        self.ts4 = TimeSeries([])

    ### Remove the database after done
    def tearDown(self):
        os.remove('testFSM.dbdb')
        del self.testFSM
        del self.ts
        del self.ts1
        del self.ts2
        del self.ts3
        del self.ts4

    ### 1. basic store and get
    def test_withKey(self):
        ### with integer id
        self.testFSM.store(ts=self.ts, id=1)
        self.assertEqual(self.testFSM.get(1), self.ts)
        self.assertEqual(self.testFSM.size(1), 5)
        ### with string idArrayTimeSeries
        self.testFSM.store(ts=self.ts, id="aaa")
        self.assertEqual(self.testFSM.get("aaa"), self.ts)
        self.assertEqual(self.testFSM.size("aaa"), 5)
        ### with ArrayTimeSeries
        self.testFSM.store(ts=self.ts3, id=2)
        self.assertEqual(self.testFSM.get(2), self.ts3)
        self.assertEqual(self.testFSM.size(2), 5)

    ### 2. duplicate id
    def test_IDAlreadyInDB(self):
        self.testFSM.store(id=1, ts=self.ts)
        self.testFSM.store(id=1, ts=self.ts1)
        self.assertEquals(self.testFSM.get(1), self.ts1)

    ### 3. ts is not timeseries
    def test_inputNotTimeseries(self):
        with self.assertRaises(TypeError):
            self.testFSM.store(ts=["aaa", 1, 5], id=1)

    ### 4. key is not found in database
    def test_wrongKey(self):
        self.testFSM.store(ts=self.ts, id=1)
        with self.assertRaises(KeyError):
            self.testFSM.get(2)
    def test_wrongKeySize(self):
        self.testFSM.store(ts=self.ts, id=1)
        with self.assertRaises(KeyError):
            self.testFSM.size(2)

class test_CreateDB(unittest.TestCase):

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

        ### with same id but different format
        self.assertEquals(self.testDB.get_ts(1), self.testDB.get_ts("1"))
        self.assertEquals(self.testDB.get_ts(1.0), self.testDB.get_ts("1.0"))
        self.assertEquals(self.testDB.get_ts("1.00"), self.testDB.get_ts("1.0"))

    ### 2. has no id
    def test_withNoID(self):
        for i in range(100):
            id_gen = self.testDB.store_ts(ts=self.ts)
        self.assertEquals(self.testDB.get_ts(id_gen), TimeSeries([-1, 0, 1.5, 4, 100], times=[0.5, 1, 2, 3, 10.5]))
        self.assertEquals(self.testDB.get_size(id_gen), 5)

    ### 3. has no time
    def test_withNoTime(self):
        self.testDB.store_ts(id=1, ts=self.ts2)
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

        # get_size should also trigger caching
        self.testDB.get_size(1)
        self.testDB.get_size(2)
        self.assertEquals(self.testDB.cache_mostAccessed, {'1': self.ts, '2': self.ts1})
        self.assertEquals(self.testDB.cache_lastAccessed, {'2': self.ts1})
        self.assertEquals(self.testDB.count_accessed, {'1': 4, '2': 3})


        # After cache is full
        self.testDB.get_ts(3)
        self.testDB.get_ts(4)
        self.testDB.get_ts(4)
        self.assertEquals(self.testDB.cache_mostAccessed, {'1': self.ts, '2': self.ts1, '4': self.ts3})
        self.assertEquals(self.testDB.cache_lastAccessed, {'4': self.ts3})
        self.assertEquals(self.testDB.count_accessed, {'1': 4, '2': 3, '3': 1, '4': 2})


## encapsulate the tests into a suite and run test as I go
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_FileStorageManager))
    suite.addTest(unittest.makeSuite(test_CreateDB))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())