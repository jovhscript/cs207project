#!/usr/bin/python3.5

import itertools
import reprlib
import numpy as np
import abstractclasses 

def isNumericList(seq):
	'''
	This function checks if the sequence parsed as argument is numeric.
	'''
	for x in seq:
		try:
			float(x)
			return True
		except:
			return False

class TimeSeries(abstractclasses.SizedContainerTimeSeriesInterface):
	"""This TimeSeries class stores a single, ordered set of numerical data as a Python list."""
	def __init__(self, values, times=None):
		"""
		The constructor of the class takes for argumnent an ordered set of numerical data.

		Parameters
		----------

		values: Numerical Sequence, compulsory
		times: Ordered Numerical Sequence, optional

		Attributes
		----------
		
		self._times: list
		self._values: list
		self.timeseries: list of tuples (time, value)

		Notes
		-----

		- If no times argument is passed, then times will be initialised by their index: 1 to len(values)

		- Errors will be raised if values or times have non numerical entries or if the times are not in ascending order
		Examples:
		---------

		>>> t1 = TimeSeries([])
		>>> t1.timeseries
		[]
		>>> t2 = TimeSeries([1, 2, 3, 4, 5])
		>>> t2.timeseries
		[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
		>>> t3 = TimeSeries([1, 2, 3], [0, 0.25, 0.5])
		>>> t3.timeseries
		[(0, 1), (0.25, 2), (0.5, 3)]
		"""

		if len(values) == 0:
			self._times = []
			self._values = []
			self.timeseries = []
		else:
			assert isNumericList(values), "Values sequence must be only contain numerical entries"
			self._values = [v for v in values]
			if times:
				assert isNumericList(times), "Time sequence must be only contain numerical entries"
				assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
				assert len(times) == len(values), "Time and Value sequences must have the same lengths"
				self._times = [t for t in times]
			else:
				self._times = range(0,len(self._values))
			self.timeseries = list(zip(self._times, self._values))

class ArrayTimeSeries(abstractclasses.SizedContainerTimeSeriesInterface):
	def __init__(self, times, values):
		assert isNumericList(values), "Values sequence must be only contain numerical entries"
		self._values = np.array([v for v in values])
		if times:
			assert isNumericList(times), "Time sequence must be only contain numerical entries"
			assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
			self._times = np.array([t for t in times])
		else:
			self._times = np.arange(0,len(self._values))
		self.timeseries = np.array(list(zip(self._times, self._values)))

	def interpolate(self, times):
		assert len(self._times) >= 1, "require at least one time-value pair for interpolation"
		assert isNumericList(times), "Time sequence must be only contain numerical entries"
		interpolated = []
		for t in times:
			if t <= self._times[0]:
				interpolated.append(self._times[0])
			elif t >= self._times[-1]:
				interpolated.append(self._times[-1])
			else:
				prev_index = np.sum(self._times < t) - 1
				lin_slope = ((self._values[prev_index + 1] - self._values[prev_index])/
					     (self._times[prev_index + 1] - self._times[prev_index]))
				interpolated_val = self._values[prev_index] + (t - self._times[prev_index]) * lin_slope
				interpolated.append(interpolated_val)
		return interpolated