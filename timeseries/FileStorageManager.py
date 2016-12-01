import series
from interfaces import *
from lab10 import DB
import numpy as np
import time

class FileStorageManager(StorageManagerInterface):
    """
    Inherits the StorageManagerInterface ABC and implements it by putting 2-d numpy arrays with 64-bit floats
    for both times and values onto disk.
    It has store, get and size methods.
    """
    def __init__(self, dbname):
        """
        Parameter:
        ----------------
        dbname: a string ending with ".dbdb"
        """
        self.db = CreateDB(dbname=dbname)

    def store(self, id, ts):
        """
        Parameters:
        ----------------
        ts (TimeSeries or ArrayTimeSeries): the timeseries to store. Has to be a valid SizedContainerTimeSeries
        id (int or str): the id for which the timeseries will be paird to

        Note:
        ----------------
        1. For more specifications of ts requirement, please see "series" for more details
        2. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        3. If a key already exist in the database, then storing a timeseries associated with that key will overwrite the
        previously stored timeseries.
        """
        self.db.store_ts(ts=ts, id=id)

    def size(self, id):
        """
        Parameters:
        ----------------
        id (int or str): the id for which the desired length's timeseries was paird to

        Returns:
        ----------------
        an interger indicating the size of the timeseries the id corresponds to

        Note:
        ----------------
        1. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        2. If the id does not exist, then a KeyError will be raised
        3. When get_size is called, the key will also trigger caching
        """
        return self.db.get_size(id=id)

    def get(self, id):
        """
        Parameters:
        ----------------
        id (int or str): the id for which the desired length's timeseries was paird to

        Returns:
        ----------------
        an timeseries instance that corresponds to the id in the database

        Note:
        ----------------
        1. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        2. If the id does not exist, then a KeyError will be raised
        3. When get_size is called, the key will also trigger caching
        """
        return self.db.get_ts(id=id)


class CreateDB:
    """
    This class create a database to store key-TimeSeries pairs with the binary tree structure laid out in lab 10.
    A few implementation details:
        - both the key and the time series are converted into strings when saved in the database. We found inconsistencies
        storing arrays and numpy arrays with lab 10's tree
        - before converted to strings, numeric keys and TimeSeries are converted into dtype numpy.float64 to ensure format
        matching (e.g. 1, 1.0, "1" are treated as the same keys)
        - caching is implemented for quick "get_ts". There are three separate caching mechanisms:
            1) most recently stored
            2) most recently accessed
            3) most frequently accessed, with size specified by user
    This class is then called by FileStorageManager, which is a much cleaner display of the underlying functionalities in CreateDB
    """
    def __init__(self, dbname, cachesize=5):
        """
        Parameters:
        ----------------
        dbname (str): the name for the database, ending in ".dbdb"
        cachesize (int): the desired size of the cache for most frequently accessed timeseries.
        """
        self.db = DB.connect(dbname)
        self.size_cache = cachesize
        self.cache_lastStored = {} # cache to store last stored timeseries (size = 1)
        self.cache_lastAccessed = {} # cache to store last accessed timeseries (size = 1)
        self.cache_mostAccessed = {} # cache to store most frequently a (size = 1)
        self.cache_mostAccessed = {} # cache to store most frequently accessed timeseries (size = cachesize)
        self.count_accessed = {} # count of each id being accessed

    def store_ts(self, ts, id=None):
        """
        Parameters:
        ----------------
        ts (TimeSeries or ArrayTimeSeries): the timeseries to store. Has to be a valid SizedContainerTimeSeries
        id (int or str): the id for which the timeseries will be paird to

        Note:
        ----------------
        1. For more specifications of ts requirement, please see "series" for more details
        2. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        3. If a key already exist in the database, then storing a timeseries associated with that key will overwrite the
        previously stored timeseries.
        """

        ### check if ts is a SizedContainerTimeSeries
        if not isinstance(ts, SizedContainerTimeSeriesInterface):
            raise TypeError('The input must be a valid timeseries')

        ### check and process id
        if id:
            id = self._encode_id(id) # convert numeric id into string
            try:
                if self.get_ts(id): # if id already exist, a message will be shown
                    print("id '{}' exists, updating its timeseries...".format(id))
            except:
                pass
        else:
            # Generate id with timestamp if the id is not provided
            id = "gen_id_{}".format(str(time.time()))

        ### add the id-timeseries pair to the database
        self.db.set(id, self._to_str(ts))
        self.db.commit()
        self.cache_lastStored = {id: ts} # save the ts into the last stored cache
        return id # the id needs to be returned in case of generated id

    def get_ts(self, id):
        """
        Parameters:
        ----------------
        id (int or str): the id for which the desired length's timeseries was paird to

        Returns:
        ----------------
        an timeseries instance that corresponds to the id in the database

        Note:
        ----------------
        1. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        2. If the id does not exist, then a KeyError will be raised
        3. When get_size is called, the key will also trigger caching
        """
        id = self._encode_id(id) # encode the id into the standardized format

        ### check if id is in each cache, from the order of last stored, last accessd to the most frequently accessed
        if id in self.cache_lastStored:
            ts = self.cache_lastStored[id]
        elif id in self.cache_lastAccessed:
            ts = self.cache_lastAccessed[id]
        elif id in self.cache_mostAccessed:
            ts = self.cache_mostAccessed[id]
        else:
            try:
                ts_str = self.db.get(id) # if id not in the cache, then pull from db
                ts = self._from_str(ts_str) # revert the stored string back to a timeseries instance
            except:
                raise KeyError("id {} not found in database".format(self._encode_id(id))) # raise an error if the id cannot be found

        self.cache_lastAccessed = {id: ts} # update the last accessed cache
        self._update_cache(id, ts) # update the most accessed cache
        return ts

    def get_size(self, id):
        """
        Parameters:
        ----------------
        id (int or str): the id for which the desired length's timeseries was paird to

        Returns:
        ----------------
        an interger indicating the size of the timeseries the id corresponds to

        Note:
        ----------------
        1. If the id appears to be a number, then it is stored as a string of numpy.float64. Foe example, 1, 1.0, "1" and
        "1.0" are all the same keys.
        2. If the id does not exist, then a KeyError will be raised
        3. When get_size is called, the key will also trigger caching
        """
        return len(self.get_ts(self._encode_id(id)))

    ### helper function to encode an id to a standardized str id
    def _encode_id(self, id):
        """
        Parameter:
        -----------------
        id: int, float or string

        Example:
        >>> print(_encode_id(1))
        1
        >>> print(_encode_id(1.0))
        1
        >>> print(_encode_id(1.1))
        1.1
        >>> print(_encode_id("1"))
        1
        >>> print(_encode_id("1.0"))
        1
        """
        try:
            id = float(id)
            if int(id) == id:
                id = int(id)
        except:
            pass
        return str(id)

    ### helper function to encode a TimeSeries into a combination of two strings of np.float64
    def _to_str(self, ts):
        """
        Parameters:
        ----------------
        ts: a TimeSeries instance passed from store_ts

        Returns:
        a string to be stored in the database
        """
        times_str = ','.join([str(t) for t in np.array(ts._times, dtype=np.float64)]) # use ',' to join times after converting to np.float64
        values_str = ','.join([str(v) for v in np.array(ts._values, dtype=np.float64)]) # use ',' to join values after converting to np.float64
        return times_str+";"+values_str

    ### helper function to decode the stored string into a TimeSeries instance
    def _from_str(self, ts_str):
        """
        Parameters:
        ----------------
        ts_str: a string looked up from get

        Returns:
        ts: a TimeSeries instance
        """
        if ts_str == ";": # empty TimeSeries
            return series.TimeSeries([])
        times_str, values_str = ts_str.split(';') # decode the two strings for times and values
        try:
            times = [float(t) for t in times_str.split(',')] # convert the string back to the float list
        except:
            raise ValueError("Cannot convert times {} into float".format(times_str))
        try:
            values = [float(v) for v in values_str.split(',')] # convert the string back to the float list
        except:
            raise ValueError("Cannot convert values {} into float".format(times_str))
        return series.TimeSeries(values=values, times=times)

    ### Helper function to update the most frequently accessed cache
    def _update_cache(self, id, ts):
        """
        Parameters:
        ----------------
        id (int or str): the standardized id passed from get_ts
        ts: the looked up timeseries passed from get_ts
        """
        if id in self.count_accessed:
            self.count_accessed[id] += 1 # add 1 to the access count if id already exist in cache
        else:
            self.count_accessed[id] = 1 # initiate the access count if id is new

        if len(self.cache_mostAccessed) < self.size_cache:
            self.cache_mostAccessed[id] = ts # when the cache is not full, keep adding the timeseries for quick access
        else:
            id_currMin = sorted(self.cache_mostAccessed, key=lambda k: self.count_accessed[k])[0] # when cache is full, sort the id's by the access count and grab the one with lowest count
            if self.count_accessed[id_currMin] < self.count_accessed[id]:
                del self.cache_mostAccessed[id_currMin] # if the corresponding min count is smaller than the current count, delete the min accessed ts in the cache
                self.cache_mostAccessed[id] = ts # and add the newest one