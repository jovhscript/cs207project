
import unittest
from series import TimeSeries

class MyTest(unittest.TestCase): 

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

	def test_tsValueTimeEqLen(self):
		'''
		Checks that the value sequence and time sequence have the same lengths
		'''
		with self.assertRaises(AssertionError):
			TimeSeries([1, 2, 3], [1])

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

	def test_interpolateInputNonNumeric(self):
		'''
		Verify that an an Error is raised if the times input to the ArrayTimeSeries interpolate method contains non numeric elements
		'''
		ts = ArrayTimeSiers([1, 2], [3, 4])
		with self.assertRaises(AssertionError):
			ts.interpolate(list('abcd'))

	def test_arrayTimeSeriesValueTimeEqLen(self):
		'''
		Checks that the value sequence and time sequence have the same lengths for ArrayTimeSeries
		'''
		with self.assertRaises(AssertionError):
			ArrayTimeSeries([1, 2, 3], [1])





if __name__ == '__main__':
    unittest.main()
