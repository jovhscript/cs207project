
import unittest
from series import TimeSeries, ArrayTimeSeries, SimulatedTimeSeries, SMTimeSeries
import numpy as np
import math

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

	def test_contains(self):
		'''
		Verify __contains__
		'''
		test_times = [2.3, 3.4, 4.1, 9, 10]
		test_values = [5, 8.9, 10.1, 19.8, 2]
		ts = TimeSeries(test_values, test_times)
		self.assertEqual((5 in ts), True)
		self.assertEqual((5.1 in ts), False)

	def test_addition(self):
		'''
		Verify adding two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = TimeSeries(test_values, test_times)
		ts0 = TimeSeries(test_values1, test_times)
		ts1 = TimeSeries(test_values1, test_times1)
		self.assertEqual((ts + ts0), TimeSeries([6, 8, 10, 12, 14], [1, 2, 3, 4, 5]))
		with self.assertRaises(ValueError):
			ts + ts1

	def test_subtraction(self):
		'''
		Verify subtracting two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = TimeSeries(test_values, test_times)
		ts0 = TimeSeries(test_values1, test_times)
		ts1 = TimeSeries(test_values1, test_times1)
		self.assertEqual((ts0 - ts), TimeSeries([4, 4, 4, 4, 4], [1, 2, 3, 4, 5]))
		with self.assertRaises(ValueError):
			ts - ts1

	def test_multiplication(self):
		'''
		Verify multiplying two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = TimeSeries(test_values, test_times)
		ts0 = TimeSeries(test_values1, test_times)
		ts1 = TimeSeries(test_values1, test_times1)
		self.assertEqual((ts * ts0), TimeSeries([5, 12, 21, 32, 45], [1, 2, 3, 4, 5]))
		with self.assertRaises(ValueError):
			ts * ts1

	def test_equal(self):
		'''
		Verify equating two timeseries
		'''
		test_times = [2.3, 3.4, 4.1, 9, 10]
		test_values = [5, 8.9, 10.1, 19.8, 2]
		test_times1 = [2, 3.4, 4.1, 9, 10]
		test_values1 = [5, 6, 7, 8, 9]
		ts = TimeSeries(test_values, test_times)
		ts0 = TimeSeries(test_values1, test_times)
		ts1 = TimeSeries(test_values1, test_times1)
		self.assertEqual((ts==ts), True)
		self.assertEqual((ts==ts0), False)
		with self.assertRaises(ValueError):
			ts == ts1

	def test_abs(self):
		'''
		Verify 2-norm of time series
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = TimeSeries(test_values, test_times)
		self.assertEqual(abs(ts), 55)

	def test_abs(self):
		'''
		Verify 2-norm of time series
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = TimeSeries(test_values, test_times)
		self.assertEqual(abs(ts), math.sqrt(55))

	def test_bool(self):
		'''
		Verify if bool of 2-norm
		'''
		test_values = [1,2,3,4,5]
		test_values1 = [0,0,0,0,0]
		ts = TimeSeries(test_values)
		ts1 = TimeSeries(test_values1)
		self.assertEqual(bool(ts), True)
		self.assertEqual(bool(ts1), False)

	def test_neg(self):
		'''
		Verify if negation
		'''
		test_values = [1,2,3,4,5]
		ts = TimeSeries(test_values)
		self.assertEqual(-ts, [-1, -2, -3, -4, -5])


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
		Checks that the value sequence and time sequence have the same lengths
		'''
		with self.assertRaises(AssertionError):
			ArrayTimeSeries([1, 2, 3], [1])



	def test_nonZeroLen(self):
		'''
		Checks we correctly render lengths
		'''
		self.assertEqual(len(ArrayTimeSeries(range(10000), range(10000))), 10000)

	def test_getItemPresent(self):
		'''
		Test the getItem with an index smaller than the length
		'''
		ts = ArrayTimeSeries([1, 2, 3], [1, 3, 5])
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

	def test_contains(self):
		'''
		Verify __contains__
		'''
		test_times = [2.3, 3.4, 4.1, 9, 10]
		test_values = [5, 8.9, 10.1, 19.8, 2]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual((5 in ts), True)
		self.assertEqual((5.1 in ts), False)

	def test_addition(self):
		'''
		Verify adding two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = ArrayTimeSeries(test_times, test_values)
		ts0 = ArrayTimeSeries(test_times, test_values1)
		ts1 = ArrayTimeSeries(test_times1, test_values1)
		assert(np.all((ts + ts0) == ArrayTimeSeries([1, 2, 3, 4, 5], [6, 8, 10, 12, 14])))
		with self.assertRaises(ValueError):
			ts + ts1

	def test_subtraction(self):
		'''
		Verify subtracting two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = ArrayTimeSeries(test_times, test_values)
		ts0 = ArrayTimeSeries(test_times, test_values1)
		ts1 = ArrayTimeSeries(test_times1, test_values1)
		assert(np.all((ts - ts0) == ArrayTimeSeries([1, 2, 3, 4, 5], [-4, -4, -4, -4, -4])))
		with self.assertRaises(ValueError):
			ts - ts1

	def test_multiplication(self):
		'''
		Verify multiplying two timeseries
		'''
		test_times = [1, 2, 3, 4, 5]
		test_values = [1, 2, 3, 4, 5]
		test_times1 = [1, 2, 3, 4, 6]
		test_values1 = [5, 6, 7, 8, 9]
		ts = ArrayTimeSeries(test_times, test_values)
		ts0 = ArrayTimeSeries(test_times, test_values1)
		ts1 = ArrayTimeSeries(test_times1, test_values1)
		assert(np.all((ts * ts0) == ArrayTimeSeries([1, 2, 3, 4, 5], [5, 12, 21, 32, 45])))
		with self.assertRaises(ValueError):
			ts * ts1

	def test_equal(self):
		'''
		Verify equating two timeseries
		'''
		test_times = [2.3, 3.4, 4.1, 9, 10]
		test_values = [5, 8.9, 10.1, 19.8, 2]
		test_times1 = [2, 3.4, 4.1, 9, 10]
		test_values1 = [5, 6, 7, 8, 9]
		ts = ArrayTimeSeries(test_times, test_values)
		ts0 = ArrayTimeSeries(test_times, test_values1)
		ts1 = ArrayTimeSeries(test_times1, test_values1)
		self.assertEqual(np.all(ts==ts), True)
		self.assertEqual(np.all(ts==ts0), False)
		with self.assertRaises(ValueError):
			ts == ts1

	def test_abs(self):
		'''
		Verify 2-norm of time series
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual(abs(ts), 55)

	def test_abs(self):
		'''
		Verify 2-norm of time series
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual(abs(ts), math.sqrt(55))

	def test_bool(self):
		'''
		Verify if bool of 2-norm
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		test_values1 = [0,0,0,0,0]
		ts = ArrayTimeSeries(test_times, test_values)
		ts1 = ArrayTimeSeries(test_times, test_values1)
		self.assertEqual(bool(ts), True)
		self.assertEqual(bool(ts1), False)

	def test_neg(self):
		'''
		Verify if negation
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual(-ts, [-1, -2, -3, -4, -5])

	def test_interpolateNumeric(self):
		'''
		Checks that an Error is raised if the time sequence input for interpolation contains non numeric elements
		'''
		test_times = [1,2,3,4,5]
		test_values = [1,2,3,4,5]
		ts = ArrayTimeSeries(test_times, test_values)
		with self.assertRaises(AssertionError):
			ts.interpolate(list('abcd'))

	def test_interpolateEmptyTS(self):
		'''
		Checks that an Error is raised if try to interpolate based on an empty ArrayTimeSeries
		'''
		ts = ArrayTimeSeries([], [])
		with self.assertRaises(AssertionError):
			ts.interpolate([1])

	def test_interpolateEmptyInput(self):
		'''
		Checks that an Error is raised if try to interpolate based on an empty ArrayTimeSeries
		'''
		ts = ArrayTimeSeries([1], [2])
		self.assertEqual(ts.interpolate([]), [])


	def test_interpolateInBound(self):
		'''
		Test the interpolate function for a new time input within the boundary of the existing time sequence
		'''
		test_times = [1,2]
		test_values = [3,6]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual(ts.interpolate([1.5]), [4.5])

	def test_interpolateBoundaryCondition(self):
		'''
		Verify if a new time point is smaller than the first time point in the existing time series, the interpolate function outputs the first value; likewise for larger time points.
		'''
		test_times = [1, 3]
		test_values = [3, 9]
		ts = ArrayTimeSeries(test_times, test_values)
		self.assertEqual(ts.interpolate([3, 5]), [9, 9])

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
