from interfaces import *
from FileStorageManager import CreateDB
import types

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

def convert_ArrayTimeSeries_to_TimeSeries(ts):
    """
    This function converts an ArrayTimeSeries to a TimeSeries instance
    """
    if isinstance(ts, ArrayTimeSeries):
        return TimeSeries(ts._values, ts._times)
    else:
        raise TypeError("input is not an ArrayTimeSeries")

def convert_TimeSeries_to_ArrayTimeSeries(ts):
    """
    This function converts a TimeSeries to an ArrayTimeSeries instance
    """
    if isinstance(ts, TimeSeries):
        return ArrayTimeSeries(ts._times, ts._values)
    else:
        raise TypeError("input is not an TimeSeries")


class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """
    This SMTimeSeries class stores a TimeSeries instance either by taking in the same parameters of TimeSeries, or
    by taking in a key and the database in which the key is associated with a TimeSeries.
    If a TimeSeries is passed into this class, then this TimeSeries instance is stored into the database where it can
    be later looked up by its key.

    Note:
    One caveat is that the attributes and methods called in TimeSeries should all be able to work with SMTimeSeries.ts,
    not SMTimeSeries itself.
    """

    def __init__(self, values=None, times=None, id=None, dbname="SMTimeSeries.dbdb"):
        """
        The constructor of the class takes for argumnent an ordered set of numerical data.

        Parameters
        ----------
        values: Numerical Sequence, compulsory
        times: Ordered Numerical Sequence, optional
        id: The ID which the TimeSeries will be stored to in the database
        dbname: Database name ending in ".dbdb"

        Notes
        -----
        - If no values are passed, then the instance rely on "from_db" method for valuation
        """
        if values is not None:
            self.db= CreateDB(dbname)
            self.ts = TimeSeries(values, times)
            self.id = self.db.store_ts(id=id, ts=self.ts)

    def from_db(self, id, dbname="SMTimeSeries.dbdb"):
        """
        The constructor of the class takes for argumnent id and database to extract a TimeSeries.

        Parameters
        ----------
        id: numeric or string key to extract timeseries. Note that this id is converted into a standardized string,
            for example: 1, 1.0, "1" and "1.0" will yield in the same id "1"
        times: Ordered Numerical Sequence, optional
        dbname: Database name ending in ".dbdb"

        Returns
        ----------
        A TimeSeries instance corresponding to the key in the specified database.
        -----
        """
        self.id = str(id)
        self.db = CreateDB(dbname)
        self.ts = self.db.get_ts(self.id)
        return self.db.get_ts(self.id)

    ### Adding computation methods for SMTimeSeries that are left to be defined
    def __add__(self, rhs):
        """
        Implementation of adding between a SMTimeSeries and another SMTimeSeries or SizedContainerTimeSeriesInterface

        Parameters:
        -----------
        rhs: a SMTimeSeries or SizedContainerTimeSeriesInterface

        Note:
        -----------
        1. The SMTimeSeries is a "more general" type; so that:
            SMT + SMT = SMT
            SMT + TS = SMT
            SMT + ATS = SMT
            TS + TS = TS
            TS + ATS = error
        2. The result is also stored in the same database, with a generated key which can be retrieved as sum.id
        """
        if isinstance(rhs, SMTimeSeries):
            out = self.ts + rhs.ts
        elif isinstance(rhs, TimeSeries):
            out = self.ts + rhs
        elif isinstance(rhs, ArrayTimeSeries):
            out = convert_ArrayTimeSeries_to_TimeSeries(convert_TimeSeries_to_ArrayTimeSeries(self.ts) + rhs)
        else:
            raise TypeError("rhs has to be a SMTimeseries or SizedContainerTimeSeriesInterface")
        return SMTimeSeries(out._values, out._times)

    def __sub__(self, rhs):
        """
        Implementation of subtracting between a SMTimeSeries and another SMTimeSeries or SizedContainerTimeSeriesInterface

        Parameters:
        -----------
        rhs: a SMTimeSeries or SizedContainerTimeSeriesInterface

        Note:
        -----------
        1. The SMTimeSeries is a "more general" type; so that:
            SMT - SMT = SMT
            SMT - TS = SMT
            SMT - ATS = SMT
            TS - TS = TS
            TS - ATS = error
        2.  The result is also stored in the same database, with a generated key which can be retrieved as sum.id
        3.  ArrayTimeSeries - SMT and TimeSeries - SMT are not yet implemented. Changes needed in ArrayTimeSeries and TimeSeries definitions
        """
        if isinstance(rhs, SMTimeSeries):
            out = self.ts - rhs.ts
        elif isinstance(rhs, TimeSeries):
            out = self.ts - rhs
        elif isinstance(rhs, ArrayTimeSeries):
            out = convert_ArrayTimeSeries_to_TimeSeries(convert_TimeSeries_to_ArrayTimeSeries(self.ts) - rhs)
        else:
            raise TypeError("rhs has to be a SMTimeseries or SizedContainerTimeSeriesInterface")
        return SMTimeSeries(out._values, out._times)

    def __mul__(self, rhs):
        """
        Implementation of multiplying between a SMTimeSeries and another SMTimeSeries or SizedContainerTimeSeriesInterface

        Parameters:
        -----------
        rhs: a SMTimeSeries or SizedContainerTimeSeriesInterface

        Note:
        -----------
        1. The SMTimeSeries is a "more general" type; so that:
            SMT * SMT = SMT
            SMT * TS = SMT
            SMT * ATS = SMT
            TS * TS = TS
            TS * ATS = error
        2.  The result is also stored in the same database, with a generated key which can be retrieved as sum.id
        """
        if isinstance(rhs, SMTimeSeries):
            out = self.ts * rhs.ts
        elif isinstance(rhs, TimeSeries):
            out = self.ts * rhs
        elif isinstance(rhs, ArrayTimeSeries):
            out = convert_ArrayTimeSeries_to_TimeSeries(convert_TimeSeries_to_ArrayTimeSeries(self.ts) * rhs)
        else:
            raise TypeError("rhs has to be a SMTimeseries or SizedContainerTimeSeriesInterface")
        return SMTimeSeries(out._values, out._times)

    def __eq__(self, rhs):
        """
        Implementation of equaling between a SMTimeSeries and another SMTimeSeries or SizedContainerTimeSeriesInterface

        Parameters:
        -----------
        rhs: a SMTimeSeries or SizedContainerTimeSeriesInterface

        Note:
        -----------
        1. The comparison will be made between the TimeSeries stored inside the SMTimeSeries, and the id does not matter
        """
        if isinstance(rhs, SMTimeSeries):
            return self.ts == rhs.ts
        if isinstance(rhs, SizedContainerTimeSeriesInterface):
            return self.ts == rhs


class TimeSeries(SizedContainerTimeSeriesInterface):
    """This TimeSeries class stores a single, ordered set of numerical data as a Python list. It inherites from the SizedContainerTimeSeriesInterface
    and hence from the TimeSeriesInterface."""
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
            if times is not None:
                assert isNumericList(times), "Time sequence must be only contain numerical entries"
                assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
                assert len(times) == len(values), "Time and Value sequences must have the same lengths"
                self._times = [t for t in times]
            else:
                self._times = range(0,len(self._values))
            self.timeseries = list(zip(self._times, self._values))

    @staticmethod
    def _check_match_helper(self , rhs):
        """
        Helper function to check if two timeseries have matching times

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; otherwise a ValueError will be raised
        """
        if (len(self._times)==0) or (len(rhs._times)==0):
            raise NotImplemented
        if not self._times==rhs._times:
            raise ValueError('self and rhs must have the same time points')

    def __add__(self, rhs):
        """
        Element-wise addition of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a + b for a, b in pairs], self._times)
        elif isinstance(rhs, (int, float)):
            return TimeSeries([x + rhs for x in self._values], self._times)
        else:
            raise TypeError('rhs must be a TimeSeries instance')

    def __sub__(self, rhs):
        """
        Element-wise subtraction of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a - b for a, b in pairs], self._times)
        elif isinstance(rhs, (int, float)):
            return TimeSeries([x - rhs for x in self._values], self._times)
        else:
            raise TypeError('rhs must be a TimeSeries instance')

    def __mul__(self, rhs):
        """
        Element-wise multiplication of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return TimeSeries([a * b for a, b in pairs], self._times)
        elif isinstance(rhs, (int, float)):
            return TimeSeries([x * rhs for x in self._values], self._times)
        else:
            raise TypeError('rhs must be a TimeSeries instance')

    def __eq__(self, rhs):
        """
        Check if two timeseries instances are the same

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, TimeSeries):
            TimeSeries._check_match_helper(self, rhs)
            pairs = zip(self._values, rhs._values)
            return all([a==b for a, b in pairs])
        else:
            raise TypeError("{} must be a TimeSeries instance".format(str(rhs)))


class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """This ArrayTimeSeries class stores a single, ordered set of numerical data as numpy arrays. It inherites from the SizedContainerTimeSeriesInterface
    and hence from the TimeSeriesInterface."""
    def __init__(self, times, values):
        """
        The constructor of the class takes for argumnent an ordered set of numerical data.

        Parameters
        ----------

        times: Ordered Numerical Sequence, compulsory
        values: Numerical Sequence, compulsory

        Attributes
        ----------
        
        self._times: numpy array
        self._values: numpy array
        self.timeseries: 2D numpy array

        Notes
        -----

        - Errors will be raised if values or times have non numerical entries or if the times are not in ascending order
        - If len(times) < len(values), the extra times are dropped
        Examples:
        ---------

        >>> t1 = ArrayTimeSeries([1, 2, 3], [1, 4, 9])
        >>> t1.timeseries
        array([[1, 1],
               [2, 4],
               [3, 9]])
        """
        if len(times) == len(values) and len(times) == 0:
            self._times = np.array([])
            self._values = np.array([])
            self.timeseries = np.array([])
        else:
            assert isNumericList(values), "Values sequence must be only contain numerical entries"
            self._values = np.array([v for v in values])
            if times is not None:
                assert isNumericList(times), "Time sequence must be only contain numerical entries"
                assert len(times) == len(values), "Time and Value sequences must have the same lengths"
                assert all(times[i] <= times[i+1] for i in range(len(times)-1)), "Time sequence must be ordered"
                self._times = np.array([t for t in times])
            else:
                self._times = np.arange(0,len(self._values))
            self.timeseries = np.array(list(zip(self._times, self._values)))
    def __json__(self):
        return {'times': [x.item() for x in self._times], 'values': [x.item() for x in self._values]}

    def interpolate(self, times):
        """
        This function returns the interpolated values for new time points entered based on the existing time-value pairs using a piecewise-linear function. 
        For every new time point input, it takes the nearest two existing time points, draws a line between them, and picks the value at the new time point. 
        
        Notes
        -----
        - It assumes stationary boundary conditions: so if a new time point is smaller than the first existing time point, it uses the first value; likewise for larger time points.
        
        Params
        ------
        times : list
        The function interpolate values for these new time points
        
        Examples
        --------
        >>> t1 = ArrayTimeSeries([1, 2], [3, 6])
        >>> t1.interpolate([1.5])
        [4.5]
        >>> t2 = ArrayTimeSeries([1, 3], [3, 9])
        >>> t2.interpolate([3, 5])
        [9, 9]
        
        """
        
        assert len(self._times) >= 1, "require at least one time-value pair for interpolation"
        if len(times) == 0:
            return []

        assert isNumericList(times), "Time sequence must only contain numerical entries"
        interpolated = []
        for t in times:  
            if t <= self._times[0]: ##The first and last items in times are the boundaries as time sequence is ordered
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

    @staticmethod
    def _check_match_helper(self , rhs):
        """
        Helper function to check if two timeseries have matching times

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; otherwise a ValueError will be raised
        """
        if (len(self._times)==0) or (len(self._times)==0):
            raise NotImplemented
        if not np.all(self._times==rhs._times):
            raise ValueError('self and rhs must have the same time points')

    def __add__(self, rhs):
        """
        Element-wise addition of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, ArrayTimeSeries):
            ArrayTimeSeries._check_match_helper(self, rhs)
            return ArrayTimeSeries(self._times, self._values + rhs._values)
        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, [x + rhs for x in self._values])
        else:
            raise TypeError('rhs must be a ArrayTimeSeries instance')

    def __sub__(self, rhs):
        """
        Element-wise subtraction of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, ArrayTimeSeries):
            ArrayTimeSeries._check_match_helper(self, rhs)
            return ArrayTimeSeries(self._times, self._values - rhs._values)
        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, [x - rhs for x in self._values])
        else:
            raise TypeError('rhs must be a ArrayTimeSeries instance')

    def __mul__(self, rhs):
        """
        Element-wise multiplication of two timeseries instances

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, ArrayTimeSeries):
            ArrayTimeSeries._check_match_helper(self, rhs)
            return ArrayTimeSeries(self._times, self._values * rhs._values)
        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, [x * rhs for x in self._values])
        else:
            raise TypeError('rhs must be a ArrayTimeSeries instance')

    def __eq__(self, rhs):
        """
        Check if two timeseries instances are the same

        Parameter
        ----------------
        rhs: a TimeSeries instance with the exact same time indeces; if rhs is not a TimeSeries, a TypeError will be raised; if the rhs does not have matching time indeces, a ValueError will be raised
        """
        if isinstance(rhs, ArrayTimeSeries):
            ArrayTimeSeries._check_match_helper(self, rhs)
            return np.all(self._values == rhs._values)
        else:
            raise TypeError('{} must be an ArrayTimeSeries instance'.format(str(rhs)))

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """ This SimulatedTimeSeries class can produce items from a time series generated by a python generator. It inherites from the StreamTimeSeriesInterface
    and hence from the TimeSeriesInterface."""
    def __init__(self, gen):
        """
        The constructor of the class takes for argumnent a generator.

        Parameters
        ----------

        gen: data generator, compulsory

        Attributes
        ----------
        
        self._gen: python generator

        Notes
        -----

        The generator can generate either tuples (time, values, ...) or single values. If it is a tuple, we will assume that the first 2 entries
        of the tuple have the (time, value) order.

        Examples:
        ---------

        >>> t1 = SimulatedTimeSeries((i, i^2) for i in range(10))
        >>> t1
        <class 'series.SimulatedTimeSeries'>
        >>> t1.produce(5)
        [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]

        """
        if not isinstance(gen, types.GeneratorType):
            raise TypeError('Must parse in a generator object.')
        self._gen = gen
    
    def produce(self, chunk=1):
        """
        The produce function generates chunks of data from a SimulatedTimeSeries
        """
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
        return self._gen
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.produce()

    def online_mean(self):
        """
        The online_mean function returns a new SimulatedTimeSeries object with a generator generating tuples (time, value, online_mean)

        Note:
        ----

        If the original generator did not generate times, the function links each (value, mean) pair with a index starting at 0.
        """
        def inner_mean(iterator=self._gen):
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
                    yield (n-1, value, mu)
        return SimulatedTimeSeries(inner_mean())

    def online_dev(self):
        """
        The online_dev function returns a new SimulatedTimeSeries object with a generator generating tuples (time, value, online_mean, std_dev)

        Note:
        ----

        If the original generator did not generate times, the function links each (value, mean, std_dev) pair with a index starting at 0.
        """
        def inner_dev(iterator=self._gen):
            n = 0
            dev_accum = 0.0
            for value in iterator:
                n += 1
                if n > 1:
                    if isinstance(value, tuple):
                        old_mu = mu
                        mu = old_mu + (value[1] - old_mu)/n
                        dev_accum += (value[1] - old_mu)*(value[1] - mu) 
                        stddev = math.sqrt(dev_accum/(n-1))
                        yield (value[0], value[1], mu, stddev)
                    else:
                        old_mu = mu
                        mu = old_mu + (value - old_mu)/n
                        dev_accum += (value - old_mu)*(value - mu) 
                        stddev = math.sqrt(dev_accum/(n-1))
                        yield (n-1, value, mu, stddev)
                else:
                    if isinstance(value, tuple):
                        mu = value[1]
                        yield (value[0], value[1], mu, 0)
                    else:
                        mu = value
                        yield (n-1, value, mu, 0)
        return SimulatedTimeSeries(inner_dev())

    def __repr__(self):
        """
        Basic repr function
        """
        return str(type(self))
        
