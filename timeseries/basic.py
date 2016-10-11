#!/usr/bin/python3.5

import itertools
import reprlib

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

class TimeSeries:
	"""This TimeSeries class stores a single, ordered set of numerical data as a Python list."""
	def __init__(self, data=None):
		"""
		The constructor of the class takes for argumnent an ordered set of numerical data.

		Parameters
		----------

		data: Ordered Sequence, optional

		Attributes
		----------

		self.timeseries: list

		Notes
		-----

		- It will raise an error if the supplied set is not ordered. If the assertion is passed,
		the constructor will store the data in a Python list in the `timeseries` attribute.

		- The constructor can handle specific cases where no data structure or an empty set is given as
		argument. It handles it by initialising the `timeseries` attribute as an empty list.

		Examples:
		---------

		>>> t1 = TimeSeries()
		>>> t2 = TimeSeries([])
		>>> t3 = TimeSeries([1, 2, 3, 4, 5])
		>>> t3.timeseries
		[1, 2, 3, 4, 5]
		>>> t4 = TimeSeries(range(500, 10000))
		"""
		if data:
			assert isNumericList(data), "Input sequence must be only contain numerical entries"
			self.timeseries = [x for x in data]
		else:
			self.timeseries = []

	def __len__(self):
		""" 
		Returns the length of the TimeSeries object, which corresponds to the length of the timeseries attribute
		"""
		return len(self.timeseries)

	def __getitem__(self, i):
		""" 
		Returns the ith item of the TimeSeries object, which corresponds to the ith item of the timeseries attribute
		
		Parameter
		---------

		i: int

		Notes
		-----

		- If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
		This is due to the fact that the underlying data structure is a Python list.
		"""

		return self.timeseries[i]

	def __setitem__(self, i, item):
		""" 
		Sets the ith item of the TimeSeries object to the value `item`

		Notes
		-----

		- If the user asks for the index of an item which is not contained in that list, an IndexError will be raised.
		This is due to the fact that the underlying data structure is a Python list.
		"""
		self.timeseries[i] = item

	def __repr__(self):
		'''
		This function returns the formal string representation of a TimeSeries object. We define the formal string
		representations by:

		Type(len=XX, timeseries=XX) 

		Notes
		-----

		- If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
		'''
		class_name = type(self).__name__
		length = len(self.timeseries)
		if length <= 5:
			return '{}(len = {}; timeseries = {})'.format(class_name, length, self.timeseries)
		else:
			components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
			components = components[:components.find(']')]
			return '{}(timeseries = {}, ...]; len = {})'.format(class_name, length, components)

	def __str__(self):
		'''
		This function returns the informal string representation of a TimeSeries object which only correponds to the
		string representation of the `timeseries` attribute.

		Notes
		-----

		- If the TimeSeries contains more than 5 elements, we only print the first 5 elements.
		'''
		length = len(self.timeseries)
		if length <= 5:
			return str(self.timeseries)
		else:
			components = reprlib.repr(list(itertools.islice(self.timeseries,0,5)))
			components = components[:components.find(']')]
			return '{}, ...]'.format(components)
