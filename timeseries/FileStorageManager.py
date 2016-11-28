from interfaces import *
from series import *
from lab10 import DB
import time

class FileStorageManager(StorageManagerInterface):
	def __init__(self, dbname):
		self.db = CreateDB(dbname=dbname)

	def store(self, id, ts):
		self.db.store_ts(ts=ts, key=id)

	def size(self, id):
		return self.db.get_size(key=id)

	def get(self, id):
		return self.db.get_ts(key=id)


class CreateDB:
	def __init__(self, dbname, cachesize=5):
		self.db = DB.connect(dbname)
		self.size_cache = cachesize
		self.cache_lastStored = {}
		self.cache_lastAccessed = {}
		self.cache_mostAccessed = {}
		self.count_accessed = {}

	def store_ts(self, ts, key=None):

		if not isinstance(ts, SizedContainerTimeSeriesInterface):
			raise ValueError('The input must be a valid timeseries')

		if key:
			key = str(key)
			# if self.get_ts(key):
			# 	print("Key exists, updating timeseries...")
			if key[:7] == 'tsSize_':
				raise ValueError("'tsSize_' is reserved for keys of timeseries sizes")
		else:
			# Generate key with timestamp
			key = "gen_key_{}".format(str(time.time()))

		self.db.set(key, self._encode_ts(ts))
		self.db.set('tsSize_'+key, str(len(ts)))
		self.db.commit()
		self.cache_lastStored = {key: ts}
		return key

	def _encode_ts(self, ts):
		times_str = ','.join([str(t) for t in ts._times])
		values_str = ','.join([str(v) for v in ts._values])
		return times_str+";"+values_str


	def _decode_ts(self, ts_str):
		if ts_str == ";":
			return TimeSeries([])
		times_str, values_str = ts_str.split(';')
		try:
			times = [float(t) for t in times_str.split(',')]
		except:
			raise ValueError("Cannot convert times {} into float".format(times_str))
		try:
			values = [float(v) for v in values_str.split(',')]
		except:
			raise ValueError("Cannot convert values {} into float".format(times_str))
		return TimeSeries(values = values, times = times)


	def get_size(self, key):
		try:
			return int(self.db.get('tsSize_'+str(key)))
		except KeyError:
			return -1


	### - two caches
	###	- one for recently added time series
	###	- the other for most commonly "get" time series


	def refresh_cache(self, key, ts):
		if key in self.count_accessed:
			self.count_accessed[key] += 1
		else:
			self.count_accessed[key] = 1

		if len(self.cache_mostAccessed) < self.size_cache:
			self.cache_mostAccessed[key] = ts
		else:
			key_currMin = sorted(self.cache_mostAccessed, key=lambda k: self.count_accessed[k])[0]
			if self.count_accessed[key_currMin] < self.count_accessed[key]:
				del self.cache_mostAccessed[key_currMin]
				self.cache_mostAccessed[key] = ts

	def get_ts(self, key):

		key = str(key)

		if key in self.cache_lastStored:
			self.cache_lastAccessed = self.cache_lastStored
			self.refresh_cache(key, self.cache_lastStored[key])
			return self.cache_lastStored[key]
		if key in self.cache_lastAccessed:
			self.refresh_cache(key, self.cache_lastAccessed[key])
			return self.cache_lastAccessed[key]
		if key in self.cache_mostAccessed:
			self.refresh_cache(key, self.cache_mostAccessed[key])
			return self.cache_mostAccessed[key]
		else:
			try:
				ts_str = self.db.get(key)
			except KeyError:
				return None

			ts = self._decode_ts(ts_str)
			self.cache_lastAccessed = {key: ts}

			### Refresh cache
			self.refresh_cache(key, ts)
			return ts