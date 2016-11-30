import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import unittest
from pytest import raises
import BinarySearchDatabase 
from generate_time_series import generate_time_series
from pick_vantage_points import pick_vantage_points
from find_most_similiar import find_most_similiar, sanity_check
import numpy as np
import math
import distances
from scipy import signal
import os

class DataBase_tests(unittest.TestCase): 
    def setUp(self):
        if os.path.isfile("/tmp/test.dbdb"):
            os.remove("/tmp/test.dbdb")
        self.db1 = BinarySearchDatabase.connect("/tmp/test.dbdb")
        self.db1.set(2,'database1')
        self.db1.set(1,'database2')
        self.db1.set(0.5,'database3')
        self.db1.set(3.2222,'database4')
        self.db1.set(4,'database5')
        self.db1.set(5,'database6')
        self.db1.set(200,'database7')
        self.db1.commit()
        self.db1.close()           
        
    def tearDown(self):
        del self.db1
        
    def test_nodes_less_than(self):
        db1 = BinarySearchDatabase.connect("/tmp/test.dbdb")
        assert (db1.get(3.2222) == 'database4')
        assert (db1.get_nodes_less_than(2) == ['database3', 'database2', 'database1'])
        assert (db1.get_nodes_less_than(4.5) == ['database3', 'database2', 'database1', 'database4', 'database5'])
        assert (db1.get_nodes_less_than(0.5) == ['database3'])
        assert (db1.get_nodes_less_than(0) == [])
        db1.close()
    
    def test_nodes_greater_than(self):
        db1 = BinarySearchDatabase.connect("/tmp/test.dbdb")
        assert (db1.get_nodes_greater_than(2) == ['database1', 'database4', 'database5', 'database6', 'database7'])
        assert (db1.get_nodes_greater_than(4.5) == ['database6', 'database7'])
        assert (db1.get_nodes_greater_than(5) == ['database6', 'database7'])
        assert (db1.get_nodes_greater_than(201) == [])    
        db1.close()
        
    def test_generate_time_series(self):
        generate_time_series()
        for i in range(1000):
            np.load("GeneratedTimeseries/Timeseries"+str(i)+".npy")
            
        with raises(FileNotFoundError):
            np.load("GeneratedTimeseries/Timeseries"+str(1000)+".npy")
            
        
    def test_pick_vantage_points(self):
        vp = np.array(pick_vantage_points())
        assert (vp >= 0).all() and (vp <= 999).all()
        for i in range(1000):
            db = BinarySearchDatabase.connect("VantagePointDatabases/"+str(i)+".dbdb")
            db.close()
            
    def test_find_most_similiar(self):
        vp = []
        with open('vp') as f:
            for line in f:
                vp.append(int(line.rstrip('\n')))

        filename = "GeneratedTimeseries/Timeseries200.npy"
        n = 20
        ans = find_most_similiar(filename, n, vp)
        ans2 = sanity_check(filename,n)
        assert ans == ans2
        
        filename = "GeneratedTimeseries/Timeseries932.npy"
        n = 3
        ans = find_most_similiar(filename, n, vp)
        ans2 = sanity_check(filename,n)
        assert ans == ans2        
                    
                              
                                  
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover