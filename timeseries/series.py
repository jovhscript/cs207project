#!/usr/bin/python3.5

import itertools
import reprlib
import numpy as np
import interfaces 

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

class TimeSeries(interfaces.SizedContainerTimeSeriesInterface):
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

class ArrayTimeSeries(interfaces.SizedContainerTimeSeriesInterface):
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


		"""
		This function returns the interpolated values for new time points entered based on the existing time-value pairs using a piecewise-linear function. 
		
		For every new time point input, it takes the nearest two existing time points, draws a line between them, and picks the value at the new time point. 
		

		Notes
		-----
		- It assumes stationary boundary conditions: so if a new time point is smaller than the first existing time point, it uses the first value; likewise for larger time points.

		Params
		------
		times : times
		The function interpolate values for these new time points
		
		Examples
		--------
		>>> t1 = ArrayTimeSeries([1, 2, 3], [3, 6, 9])
		>>> t1.interpolate([1.5, 5])
		[4.5, 9]

		"""

        assert len(self._times) >= 1, "require at least one time-value pair for interpolation"
        assert isNumericList(times), "Time sequence must be only contain numerical entries"
        interpolated = []
        for t in times:
            if t <= self._times[0]: "The first and last items in times are the boundaries as time sequence is ordered"
                interpolated.append(self._values[0])
            elif t >= self._times[-1]:
                interpolated.append(self._values[-1])
            else:
                prev_index = np.sum(self._times < t) - 1
                lin_slope = ((self._values[prev_index + 1] - self._values[prev_index])/
                         (self._times[prev_index + 1] - self._times[prev_index]))
                interpolated_val = self._values[prev_index] + (t - self._times[prev_index]) * lin_slope
                interpolated.append(interpolated_val)
        return interpolated

class SimulatedTimeSeries(interfaces.StreamTimeSeriesInterface):
    
    def __init__(self, gen):
        self._gen = gen
    
    def produce(self, chunk=1):
        val_array = []
        try:
            for i in range(0, chunk):
                next_value = next(self._gen)
                val_array.append(next_value)
        except:
            pass
        finally:
            return val_array
    
    def iteritems(self):
        return self.produce()[1]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.produce()

    def online_mean(self):
        def inner(iterator=self._gen):
            n = 0
            mu = 0
            for value in iterator:
                n += 1
                if isinstance(value, tuple):
                    delta = value[1] - mu
                    mu = mu + delta/n
                    yield (value[0], value[1], mu)
                else:
                    delta = value - mu
                    mu = mu + delta/n
                    yield (n, value[1], mu)
        return SimulatedTimeSeries(inner())

    def online_dev(iterator):
        def inner(iterator=self._gen):
            n = 0
            dev_accum = 0.0
            for value in iterator:
                n += 1
                if n > 1:
                    old_mu = mu
                    mu = old_mu + (value - old_mu)/n
                    dev_accum += (value - old_mu)*(value - mu) 
                    stddev = sqrt(dev_accum/(n-1))
                    yield (n, value, mu, stddev)
                else:
                    mu = value
            yield (n, value, mu, 0.0) 
        return SimulatedTimeSeries(inner())

    def __repr__(self):
        return str(type(self))
        
