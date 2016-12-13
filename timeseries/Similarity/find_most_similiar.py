import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import numpy as np
import random
import BinarySearchDatabase
import RedBlackSearchDatabase
from series import ArrayTimeSeries as ts
import os
import distances
import sys
#from pick_vantage_points import pick_vantage_points
import pickle
import argparse
import shutil
from tsdb_error import *


def sanity_check(filename,n):
    """
    Function that manually finds the n most similiar timeseries to the given
    timeseries. Serves as a check of the vantage point method
    
    Returns: list of n most similiar filenames 
    """
    ans = []
    d = []
    with open(filename, "rb") as f:
        ts1 = pickle.load(f)
    
    for i in range(1000):
        with open("GeneratedTimeseries/Timeseries"+str(i), "rb") as f:
            ts2 = pickle.load(f)     
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        d.append([dist,"Timeseries"+str(i)])
        
    d.sort(key=lambda x: x[0])
    for i in range(1,n+1):
        ans.append(d[i][1])
        
    return ans


def find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius, dbtype='bstree'):
    """
    Given a vantage point and a radius, find the points that fall within the
    circle around the vantage point. Then calculates the distance from all of these
    points to the timeseries of interest.
    
    closest_vantage_pt: number of the vantage point being considered
    ts1: timeseries of interest
    radius: radius of circle to consider
    
    Returns: list of tuples (distance, timeseries id) in sorted order
    """
    if dbtype == 'bstree':
        dbdir = 'VantagePointDatabases'
        #open database for that vantage point
        db = BinarySearchDatabase.connect("%s/%s.dbdb"%(dbdir, str(closest_vantage_pt)))
    elif dbtype == 'rbstree':
        dbdir = 'VantagePointDatabases_RedBlack'
        #open the redblacksearch database for that vantage point
        db = RedBlackSearchDatabase.connect("%s/%s.dbdb"%(dbdir, str(closest_vantage_pt)))
    #open database for that vantage point
    
    #find all light curves within 2d of the vantage point
    light_curves_in_radius = db.get_nodes_less_than(radius)
    light_curves_in_radius.append(str(closest_vantage_pt)) # add in the vantage pt
    db.close()    
    
    #find similiarity between these light curves and given light curve
    distance = []
    for l in light_curves_in_radius:
        with open("GeneratedTimeseries/Timeseries"+str(l), "rb") as f:
            ts2 = pickle.load(f)
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        distance.append([dist,"Timeseries"+str(l)]) 
    return distance

def find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius, dbtype = 'bstree'):
    """
    Given a vantage point and a radius, find the points that fall within the
    circle around the vantage point. Then calculates the distance from all of these
    points to the timeseries of interest.
    
    closest_vantage_pt: number of the vantage point being considered
    ts1: timeseries of interest
    radius: radius of circle to consider
    
    Returns: list of tuples (distance, timeseries id) in sorted order
    """

    if dbtype == 'bstree':
        dbdir = 'VantagePointDatabases'
        #open database for that vantage point
        db = BinarySearchDatabase.connect("%s/%s.dbdb"%(dbdir, str(closest_vantage_pt)))
    elif dbtype == 'rbstree':
        dbdir = 'VantagePointDatabases_RedBlack'
        #open the redblacksearch database for that vantage point
        db = RedBlackSearchDatabase.connect("%s/%s.dbdb"%(dbdir, str(closest_vantage_pt)))

    #find all light curves within 2d of the vantage point
    light_curves_in_radius = db.get_nodes_less_than(radius)
    light_curves_in_radius.append(str(closest_vantage_pt)) # add in the vantage pt
    db.close()    
    
    #find similiarity between these light curves and given light curve
    distance = []
    for l in light_curves_in_radius:
        with open("GeneratedTimeseries/Timeseries"+str(l), "rb") as f:
            ts2 = pickle.load(f)
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        distance.append([dist,"Timeseries"+str(l)]) 
    return distance

def interpolate_to_match_input(ts_database, ts_input):
    """
    interpolate the generated timeseries in the database to match the timeseries
    input from the client
    
    Parameter
    ----------------
    ts_input: timeseries input by the client
    ts_database: the timeseries generated in the database
    """
    ts_input_times = ts_input.times()
    ts_database_times = ts_database.times()
    interpolated_values = ts_database.interpolate(ts_input_times)
    interpolated_ts = ts(ts_input_times, interpolated_values)
    return interpolated_ts

def find_most_similiar(filename,n, vantage_pts, isfile=True, dbtype = 'bstree'):
    """
    Finds n most similiar time series to the time series of interest (filename)
    by using the supplied vantage points
    
    filename: timeseries of interest
    n: number of similiar timeseries to return (n must be between 1 and 20)
    vantage_pts: a list of the vantage point numbers 
    
    Returns: list of n most similiar filenames
    """
    
    file_names = []
    #load the given file
    if isfile:
        try:
            with open(filename, "rb") as f:
                ts1 = pickle.load(f)
        except:
            print ('Requested %s cannot be found in database, returning ERROR INDEX'%filename)
            return 'ERROR INDEX'
    else:
        ts1 = filename

    ## check data type
    if not isinstance(ts1, ts):
        print ('Requested %s is not a TimeSeries instance, returning ERROR TYPE'%filename)
        return 'ERROR TYPE'
       
    #find the most similiar vantage point = d 
    vantage_pts_dist = []
    for i in vantage_pts:
        with open("GeneratedTimeseries/Timeseries"+str(i), "rb") as f:
            ts2 = pickle.load(f)

        ## interpolate the timeseries in the database to have the same times
        ## as the client input timeseries
        ts2 = interpolate_to_match_input(ts2, ts1)

        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        vantage_pts_dist.append([dist,i])
    if n>len(vantage_pts_dist) or n<1:
        print('More neighbours than vantage requested.')
        return 'ERROR NUMBER | {}'.format(len(vantage_pts_dist))
    vantage_pts_dist.sort(key=lambda x: x[0])
    
    all_pts_to_check = []
    for i in range(n):
        closest_vantage_pt = vantage_pts_dist[i][1]
        radius = 2*vantage_pts_dist[i][0]
        pts_in_radius = find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius, dbtype)
        for j in pts_in_radius:
            if j not in all_pts_to_check:
                all_pts_to_check.append(j)
                
    all_pts_to_check.sort(key=lambda x: x[0])

    for i in range(0,n): #ignore given timeseries
        file_names.append(all_pts_to_check[i])  
        
    return file_names

def similarity_program(arg, dbtype = 'bstree'):
    """This is a command line program that finds similiar timeseries"""
    if dbtype == 'bstree':
        dbdir = 'VantagePointDatabases'
    elif dbtype == 'rbstree':
        dbdir = 'VantagePointDatabases_RedBlack'

    vp = []
    with open('%s/vp'%dbdir) as f:
        for line in f:
            vp.append(int(line.rstrip('\n')))    
    
    parser = argparse.ArgumentParser(description="TimeSeries Similiarity Search")
    parser.add_argument('timeseries', help="TimeSeries", type=str)
    parser.add_argument('--n', help='finds n most similiar timeseries', type=int, default=1)
    parser.add_argument('--save', help='Save results?', type=bool, default=False)
    parser.add_argument('--savefolder', help='Where to save result', type=str, default='SimilaritySearchResults')
    
    args = parser.parse_args(arg)
    input_var = "GeneratedTimeseries/"+args.timeseries
    n = args.n
    save = args.save
    savefolder = args.savefolder

    #Ensure that the file given is valid
    if not os.path.isfile(input_var):
        return "Invalid timeseries filename"
      
    if n < 1 or n > len(vp):
        return "N must be between 1 and # vantage points"
          
    
    ts = find_most_similiar(input_var,n, vp)
    
    if save == True:
        if os.path.isdir(savefolder):
            shutil.rmtree(savefolder)
            os.mkdir(savefolder) 
        else:
            os.mkdir(savefolder)          

        for i in ts:
            with open("GeneratedTimeseries/"+str(i), "rb") as f:
                ts1 = pickle.load(f)
            with open(str(savefolder)+"/"+str(i),'wb') as f2:
                pickle.dump(ts1, f2)
    else:
        print(ts)
                        
        

if __name__ == "__main__":
    similarity_program(sys.argv[1:])
        

            
    
    
    
    
       
    
    



