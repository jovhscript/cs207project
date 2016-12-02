import sys
import os.path
import shutil
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import distances
import numpy as np
import random
import BinarySearchDatabase
from series import ArrayTimeSeries as ts
import os
import pickle
import argparse

def pick_vantage_points(arg):
    """
    Code which picks 20 vantage points and produces a database for each one.
    The database stores (key,value) pairs where:
    key = distance from timeseries to vantage point (kernel coefficient)
    value = id of timeseries (0-999)
    
    returns: list of vantage points (integers from 0-999)
    """
    try:
        parser = argparse.ArgumentParser(description="vantage points")
        parser.add_argument('--n', help='number of vantage points', type=int, default=20)
            
        args = parser.parse_args(arg)
        num = args.n
    except:
        num = arg
    
    try:
        shutil.rmtree('VantagePointDatabases')
        os.mkdir('VantagePointDatabases')    
    except:
        os.mkdir('VantagePointDatabases')    
        
    
    vantage_pts = random.sample(range(0,1000),num)

    for vantage_point in vantage_pts:
        try:
            os.remove("VantagePointDatabases/"+str(vantage_point)+".dbdb")
            db1 = BinarySearchDatabase.connect("VantagePointDatabases/"+str(vantage_point)+".dbdb")
        except:
            db1 = BinarySearchDatabase.connect("VantagePointDatabases/"+str(vantage_point)+".dbdb")
        
        with open("GeneratedTimeseries/Timeseries"+str(vantage_point), "rb") as f:
            ts2 = pickle.load(f)
        for i in range(1000):
            if i != vantage_point:
                with open("GeneratedTimeseries/Timeseries"+str(i), "rb") as f:
                    ts1 = pickle.load(f)
                dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
                db1.set(dist,str(i))
    
        db1.commit()
        db1.close()
        
        f = open('VantagePointDatabases/vp', 'w')
        for i in vantage_pts:
            f.write(str(i)+"\n")
        f.close()
        
    return vantage_pts    

if __name__ == "__main__":
    pick_vantage_points(sys.argv[1:])
    