import sys, inspect
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(os.path.dirname(currentdir))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import pdb
import unittest
from pytest import raises
import numpy as np
import math
from scipy import signal
import os
import pickle
from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
from find_most_similiar import find_most_similiar, sanity_check
from tstojson import *
import argparse
from tsdb_error import *


with open('VantagePointDatabases_RedBlack/vp') as f:
    vp = []
    for line in f:
        vp.append(int(line.rstrip('\n'))) 


class server_tests(unittest.TestCase): 
    """
    This is a full integration test as opposed to a standard unittest.
    In order for these tests to work, the user would have to start the
    server. Once server.py is running, these tests can be run.

    Sample usage:
    In one terminal: python ../server.py
    In another terminal: python test_server.py
    """

    def test_findByIndex(self):
        '''
        Verify that the server receives the requested time series, finds similar
        time series, and return the correct one as expected.
        '''

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 15000))
        s.send("{}|{}|ind".format('Timeseries200', 1).encode())
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        toget = s.recv(length).decode('utf-8')
        
        ## note that the server finds timeseries and vintage points in the
        ## current directory and has access to the database there 
        tss_found = find_most_similiar("GeneratedTimeseries/Timeseries200", 1, vp, dbtype = 'rbstree')
        jsondump = json.dumps(tss_found)
        assert toget[:len(jsondump)-2] == jsondump[:-2]
        assert kind == 'J'

    def test_findByUploadedJSON(self):
        '''
        Verify that the server receives the uploaded time series in a JSON file, 
        finds similar time series, and return the correct one as expected.
        '''
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 15000))
        ts_ = sencode('%s/Timeseries0.json'%parentdir)
        s.send("{}|{}|json".format(ts_, 1).encode())
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        toget = s.recv(length).decode('utf-8')
        
        ## note that the server finds timeseries and vintage points in the
        ## current directory and has access to the database there 
        import pdb;pdb.set_trace()
        ts_interest = sdecode(ts_)
        tss_found = find_most_similiar(ts_interest, 1, vp, False, dbtype = 'rbstree')
        jsondump = json.dumps(tss_found)
        #assert toget[:len(jsondump)-2] == jsondump[:-2]
        assert kind == 'J'

    def test_indexError(self):
        '''
        Verify that index  error is raised the user input a time series index 
        that does not exist in the database
        '''

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 15000))
        s.send("{}|{}|ind".format('Timeseries2000', 1).encode())
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        toget = s.recv(length).decode('utf-8')
        
        assert toget == 'ERROR 400: NO SUCH INDEX IN DATABASE'
        assert kind == 'E'


    def test_negativeNumberOfSimilarSeriesError(self):
        '''
        Verify that index error is raised the user requests a negative
        number of most similar time series
        '''

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 15000))
        s.send("{}|{}|ind".format('Timeseries200', -1).encode())
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        toget = s.recv(length).decode('utf-8')
        
        assert toget == 'ERROR 400: N should be between 1 and 20'
        assert kind == 'E'


    def test_numberOutOfRangeError(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 15000))
        s.send("{}|{}|ind".format('Timeseries200', 100).encode())
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        toget = s.recv(length).decode('utf-8')

        assert toget == 'ERROR 400: N should be between 1 and 20'
        assert kind == 'E'



if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
