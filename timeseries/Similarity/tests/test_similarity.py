import sys, inspect
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir) 

import unittest
from pytest import raises
from series import TimeSeries, ArrayTimeSeries, SimulatedTimeSeries
from series import ArrayTimeSeries as ts
import numpy as np
import math
import distances
from scipy import signal

class SimilarityTest(unittest.TestCase):   
        
    def test_tsmakers(self):
        t1 = distances.tsmaker(0.5, 0.1, 0.01)
        assert type(t1) == ts #make sure tsmaker returns correct type
        t2 = distances.random_ts(0.5)
        assert type(t2) == ts #make sure random_ts returns correct type 
        
    def test_standardize(self):
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        assert t0.mean() == 5.5 #check mean
        assert t0.std() == np.sqrt(17.5/6.0) #check sqrt
        
        standardized_values = distances.stand(t0,t0.mean(),t0.std()).values()
        assert (str(standardized_values) == str(np.array([-1.46385011,-0.87831007,-0.29277002,0.29277002,0.87831007,1.46385011]))) #check that standardized values are correct

    def test_standardizeConstant(self):
        t0 = ts(times=[0,1,2,4,5,6],values=[3,3, 3, 3, 3, 3])
        standardized_values = distances.stand(t0,t0.mean(),t0.std()).values()
        assert (str(standardized_values) == str(np.array([0.,0.,,0.,0.,0.]))) #check that standardize a series of constant return a series of zeros

        
    def test_ccor(self):
        t0 = ts(times=[0,1,2,3],values=[1,2,3,4])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,3],values=[-1,2,1,-1])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())
        d = distances.ccor(t0_stand,t1_stand)
        assert (str(d) == str(np.array([0.25819889,-0.94672926,-0.0860663,0.77459667])))
        
    def test_maxcorratphase(self):
        t0 = ts(times=[0,1,2,3],values=[1,2,3,4])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,3],values=[-1,2,1,-1])
        t1_stand = distances.stand(t1,t1.mean(), t1.std()) 
        assert (distances.max_corr_at_phase(t0_stand,t1_stand)) == (3, 0.77459666924148329)
        
    def test_kernelcorr(self):
        """tests that the kernelized cross correlation is 1 when
        the two timeseries are identical"""
        
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())   
        assert distances.kernel_corr(t1_stand, t0_stand) == 1
        
        t3 = ts(times=[0,1,2,4,5,6],values=[3,7,9,10,16,20])
        t3_stand = distances.stand(t3,t3.mean(), t3.std())          
        assert (distances.kernel_corr(t1_stand, t3_stand) < 1)
        
    def test_distance(self):
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())        
        assert distances.distance(t0_stand, t1_stand) == 0
        
        
        
        
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
