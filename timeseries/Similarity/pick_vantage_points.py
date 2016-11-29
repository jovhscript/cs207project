import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import distances
import numpy as np
import random
import BinarySearchDatabase
from series import ArrayTimeSeries as ts
import os

def pick_vantage_points():
    """
    Code which picks 20 vantage points and produces a database for each one.
    The database stores (key,value) pairs where:
    key = distance from timeseries to vantage point (kernel coefficient)
    value = id of timeseries (0-999)
    
    returns: list of vantage points (integers from 0-999)
    """
    vantage_pts = random.sample(range(0,1000),20)

    for vantage_point in vantage_pts:
        try:
            os.remove("VantagePointDatabases/"+str(vantage_point)+".dbdb")
            db1 = BinarySearchDatabase.connect("VantagePointDatabases/"+str(vantage_point)+".dbdb")
        except:
            db1 = BinarySearchDatabase.connect("VantagePointDatabases/"+str(vantage_point)+".dbdb")
        
        two = np.load("GeneratedTimeseries/Timeseries"+str(vantage_point)+".npy")
        for i in range(1000):
            if i != vantage_point:
                one = np.load("GeneratedTimeseries/Timeseries"+str(i)+".npy")
                ts1 = ts(times=one[0],values=one[1])
                ts2 = ts(times=two[0],values=two[1])
                dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
                #print(dist)
                db1.set(dist,str(i))
    
        db1.commit()
        db1.close()
        
        f = open('vp', 'w')
        for i in vantage_pts:
            f.write(str(i)+"\n")
        f.close()
        
    return vantage_pts    

if __name__ == "__main__":
    pick_vantage_points()