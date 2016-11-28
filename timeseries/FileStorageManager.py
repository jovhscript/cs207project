import series
from interfaces import *
from lab10 import DB
import numpy as np
import time

class FileStorageManager(StorageManagerInterface):
    def __init__(self, dbname):
        self.db = CreateDB(dbname=dbname)

    def store(self, id, ts):
        self.db.store_ts(ts=ts, id=id)

    def size(self, id):
        return self.db.get_size(id=id)

    def get(self, id):
        return self.db.get_ts(id=id)


class CreateDB:
    def __init__(self, dbname, cachesize=5):
        self.db = DB.connect(dbname)
        self.size_cache = cachesize
        self.cache_lastStored = {}
        self.cache_lastAccessed = {}
        self.cache_mostAccessed = {}
        self.count_accessed = {}

    def store_ts(self, ts, id=None):

        if not isinstance(ts, SizedContainerTimeSeriesInterface):
            raise TypeError('The input must be a valid timeseries')

        if id:
            id = str(id)
            # if self.get_ts(id):
            # 	print("Key exists, updating timeseries...")
            if id[:7] == 'tsSize_':
                raise ValueError("'tsSize_' is reserved for ids of timeseries sizes")
        else:
            # Generate id with timestamp
            id = "gen_id_{}".format(str(time.time()))

        self.db.set(id, self._encode_ts(ts))
        self.db.set('tsSize_'+id, str(len(ts)))
        self.db.commit()
        self.cache_lastStored = {id: ts}
        return id

    def _encode_ts(self, ts):
        times_str = ','.join([str(t) for t in np.array(ts._times, dtype=np.float64)])
        values_str = ','.join([str(v) for v in np.array(ts._values, dtype=np.float64)])
        return times_str+";"+values_str


    def _decode_ts(self, ts_str):
        if ts_str == ";":
            return series.TimeSeries([])
        times_str, values_str = ts_str.split(';')
        try:
            times = [float(t) for t in times_str.split(',')]
        except:
            raise ValueError("Cannot convert times {} into float".format(times_str))
        try:
            values = [float(v) for v in values_str.split(',')]
        except:
            raise ValueError("Cannot convert values {} into float".format(times_str))
        return series.TimeSeries(values=values, times=times)


    def get_size(self, id):
        try:
            return int(self.db.get('tsSize_'+str(id)))
        except KeyError:
            return -1


    ### - two caches
    ###	- one for recently added time series
    ###	- the other for most commonly "get" time series


    def refresh_cache(self, id, ts):
        if id in self.count_accessed:
            self.count_accessed[id] += 1
        else:
            self.count_accessed[id] = 1

        if len(self.cache_mostAccessed) < self.size_cache:
            self.cache_mostAccessed[id] = ts
        else:
            id_currMin = sorted(self.cache_mostAccessed, key=lambda k: self.count_accessed[k])[0]
            if self.count_accessed[id_currMin] < self.count_accessed[id]:
                del self.cache_mostAccessed[id_currMin]
                self.cache_mostAccessed[id] = ts

    def get_ts(self, id):

        id = str(id)

        if id in self.cache_lastStored:
            self.cache_lastAccessed = self.cache_lastStored
            self.refresh_cache(id, self.cache_lastStored[id])
            return self.cache_lastStored[id]
        elif id in self.cache_lastAccessed:
            self.refresh_cache(id, self.cache_lastAccessed[id])
            return self.cache_lastAccessed[id]
        elif id in self.cache_mostAccessed:
            self.refresh_cache(id, self.cache_mostAccessed[id])
            return self.cache_mostAccessed[id]
        else:
            try:
                ts_str = self.db.get(id)
            except KeyError:
                return None


        ts = self._decode_ts(ts_str)
        self.cache_lastAccessed = {id: ts}

        ### Refresh cache
        self.refresh_cache(id, ts)
        return ts