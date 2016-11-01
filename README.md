# cs207project

This is a library for performing time series analysis. Functional python files are found in the timeseries folder, and divided amongst five key files:

1) interfaces.py : Interface classes are found in this file, namely TimeSeriesInterface, SizedContainerTimeSeriesInterface, and StreamTimeSeriesInterface.

2) lazy.py : A class performing a lazy-computed time series is found in this file. 

3) series.py : Classes that will be called and interacted with from the user are found in this file, namely TimeSeries, ArrayTimeSeries, and SimulatedTimeSeries.

4) SmokeTest.py : A basic smoke test for the primary functionality of the library is implemented in this file.

5) test_basic.py : This file contains all the unit tests for time series classes in the library.

CONTRIBUTORS:

The primary authors of this library are Virgile Audi, Omar Abboud, Jack Qian, and Heidi Chen. This library was created as part of course CS207 - Systems Development for Computational Science at the Harvard University Institute for Applied Computational Science.