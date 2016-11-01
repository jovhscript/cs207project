
import unittest
from series import TimeSeries, ArrayTimeSeries, SimulatedTimeSeries
import numpy as np

class TimeSeriesTest(unittest.TestCase): 
	"""
	These tests concern the TimeSeries Class
	"""
	def test_noArgument(self):
		'''
		Verify that an error is raised when no values argument is passed
		'''
		with self.assertRaises(TypeError):
			ts = TimeSeries()

	def test_emptyList(self):
		'''
		Verify that empty timeseries is constructed when empty sequence is given
		'''
		ts = TimeSeries([])
		self.assertEqual(ts.timeseries, [])

	def test_range(self):
		'''
		Verify that "unrealized" sequences can be parsed as argument
		'''
		ts = TimeSeries(range(1, 10, 2))
		self.assertEqual(ts.timeseries, [(0, 1), (1, 3), (2, 5), (3, 7), (4, 9)])

	def test_nonNumeric(self):
		'''
		Checks that an Error is raised if the sequence contains non numeric elements
		'''
		with self.assertRaises(AssertionError):
			TimeSeries(list('abcd'))

	def test_valTimeEqLen(self):
		'''
		Checks that the value sequence and time sequence have the same lengths
		'''
		with self.assertRaises(AssertionError):
			TimeSeries([1, 2, 3], [1])

	def test_zeroLen(self):
		'''
		Checks we correctly render 0 length
		'''
		self.assertEqual(len(TimeSeries([])), 0)

	def test_nonZeroLen(self):
		'''
		Checks we correctly render lengths
		'''
		self.assertEqual(len(TimeSeries(range(10000))), 10000)

	def test_getItemPresent(self):
		'''
		Test the getItem with an index smaller than the length
		'''
		ts = TimeSeries([1, 2, 3, 4, 5])
		self.assertEqual(ts[2], 3)

	def test_getItemNotPresent(self):
		'''
		Verify that an IndexError is raised when trying to access an element not contained in the TimeSeries
		'''
		ts = TimeSeries([1, 2, 3, 4, 5])
		with self.assertRaises(IndexError):
			ts[10]

	def test_setItemPresent(self):
		'''
		Verify we can change an element in the list
		'''
		ts = TimeSeries([0,1,2,3,4])
		ts[4] = 10
		self.assertEqual(ts[4], 10)

	def test_setItemNonPresent(self):
		'''
		Verify that an IndexError is raised when trying to change the value of an element that is not present in the TimeSeries object
		'''
		ts = TimeSeries([])
		with self.assertRaises(IndexError):
			ts[0] = 10

class ArrayTimeSeriesTest(unittest.TestCase): 
	"""
	These tests concern the ArrayTimeSeries
	"""
	def test_noArgument(self):
		'''
		Verify that an error is raised when no arguments is passed
		'''
		with self.assertRaises(TypeError):
			ts = ArrayTimeSeries()

	def test_oneArgument(self):
		'''
		Verify that an error is raised when no values argument is passed
		'''
		with self.assertRaises(TypeError):
			ts = ArrayTimeSeries([])

	def test_emptyList(self):
		'''
		Verify that empty timeseries is constructed when empty sequences are given
		'''
		ts = ArrayTimeSeries([], [])
		self.assertTrue(np.array_equal(ts.timeseries, np.array([])))

	def test_range(self):
		'''
		Verify that "unrealized" sequences can be parsed as argument
		'''
		ts = ArrayTimeSeries(range(1, 10, 2), range(1, 10, 2))
		self.assertTrue(np.array_equal(ts.timeseries, np.array([[1, 1], [3, 3], [5, 5], [7, 7], [9, 9]])))

	def test_nonNumeric(self):
		'''
		Checks that an Error is raised if the sequence contains non numeric elements
		'''
		with self.assertRaises(AssertionError):
			ArrayTimeSeries(list('abcd'), list('abcd'))

	def test_valTimeEqLen(self):
		'''
		Checks that when value sequence and time sequence do not have the same lengths, extra times are dropped
		'''
		ts = ArrayTimeSeries([1, 2, 3], [1])
		self.assertTrue(np.array_equal(ts.timeseries, np.array([[1, 1]])))

	def test_nonZeroLen(self):
		'''
		Checks we correctly render lengths
		'''
		self.assertEqual(len(ArrayTimeSeries(range(10000), range(10000))), 10000)

	def test_getItemPresent(self):
		'''
		Test the getItem with an index smaller than the length
		'''
		ts = ArrayTimeSeries([1, 2, 3], [1])
		self.assertEqual(ts[0], 1)

	def test_getItemNotPresent(self):
		'''
		Verify that an IndexError is raised when trying to access an element not contained in the ArrayTimeSeries
		'''
		ts = ArrayTimeSeries([1, 2, 3], [1, 2, 6])
		with self.assertRaises(IndexError):
			ts[10]

	def test_setItemPresent(self):
		'''
		Verify we can change an element in the timeseries without changing its time.
		'''
		ts = ArrayTimeSeries([0,1,2,3,4], [0,1,2,3,4])
		ts[4] = 10
		self.assertTrue(ts[4]==10 and ts._times[4]==4)

	def test_setItemNonPresent(self):
		'''
		Verify that an IndexError is raised when trying to change the value of an element that is not present in the ArrayTimeSeries object
		'''
		ts = ArrayTimeSeries([], [])
		with self.assertRaises(IndexError):
			ts[0] = 10

class StreamingTimeSeriesTest(unittest.TestCase):
	"""
	These tests concern the SimulatedTimeSeries class.
	"""
	def test_noArgument(self):
		'''
		Verify that a TypeError is raised if no generator is parsed
		'''
		with self.assertRaises(TypeError):
			SimulatedTimeSeries()

	def test_notGenerator(self):
		'''
		Verify that a TypeError is raised if an object other than a generator is parsed
		'''
		with self.assertRaises(TypeError):
			SimulatedTimeSeries([i for i in range(10)])

	def test_valueOnlyGenerator(self):
		'''
		Check that we can produce timeseries with value only generator
		'''
		ts = SimulatedTimeSeries((i**2 for i in range(100)))
		self.assertEqual(ts.produce(10), [0, 1, 4, 9, 16, 25, 36, 49, 64, 81])

	def test_timeValueGenerator(self):
		'''
		Check that we can produce timeseries with value only generator
		'''
		ts = SimulatedTimeSeries(((i,i**2) for i in range(100)))
		self.assertEqual(ts.produce(10), [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81)])

	def test_onlineMeanTime(self):
		'''
		Verifies the online_mean function when times are generated
		'''
		ts = SimulatedTimeSeries(((i,i**2) for i in range(100)))
		om = ts.online_mean()
		self.assertEqual(om.produce(5), [(0, 0, 0.0), (1, 1, 0.5), (2, 4, 1.6666666666666667), (3, 9, 3.5), (4, 16, 6.0)])

	def test_onlineMeanNoTime(self):
		'''
		Verifies the online_mean function when no times are generated
		'''
		ts = SimulatedTimeSeries((i**2 for i in range(100)))
		om = ts.online_mean()
		self.assertEqual(om.produce(5), [(0, 0, 0.0), (1, 1, 0.5), (2, 4, 1.6666666666666667), (3, 9, 3.5), (4, 16, 6.0)])

	def test_onlineDevTime(self):
		'''
		Verifies the online_dev function when no times are generated
		'''
		ts = SimulatedTimeSeries(((i, i**2) for i in range(100)))
		od = ts.online_dev()
		self.assertEqual(od.produce(5), [(0, 0, 0, 0), (1, 1, 0.5, 0.7071067811865476), (2, 4, 1.6666666666666667, 2.0816659994661326), (3, 9, 3.5, 4.041451884327381), (4, 16, 6.0, 6.59545297913646)])

	def test_onlineDevNoTime(self):
		'''
		Verifies the online_mean function when no times are generated
		'''
		ts = SimulatedTimeSeries((i**2 for i in range(100)))
		od = ts.online_dev()
		self.assertEqual(od.produce(5), [(0, 0, 0, 0), (1, 1, 0.5, 0.7071067811865476), (2, 4, 1.6666666666666667, 2.0816659994661326), (3, 9, 3.5, 4.041451884327381), (4, 16, 6.0, 6.59545297913646)])
		
def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TimeSeriesTest))
	suite.addTest(unittest.makeSuite(ArrayTimeSeriesTest))
	suite.addTest(unittest.makeSuite(StreamingTimeSeriesTest))
	return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
