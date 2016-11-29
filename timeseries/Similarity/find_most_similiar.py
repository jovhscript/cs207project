import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import numpy as np
import random
import BinarySearchDatabase
from series import ArrayTimeSeries as ts
import os
import distances
import sys
from pick_vantage_points import pick_vantage_points


def sanity_check(filename,n):
    """
    Function that manually finds the n most similiar timeseries to the given
    timeseries. Serves as a check of the vantage point method
    
    Returns: list of n most similiar filenames 
    """
    ans = []
    d = []
    given_file = np.load(filename)
    ts1 = ts(times=given_file[0],values=given_file[1]) 
    
    for i in range(1000):
        two = np.load("GeneratedTimeseries/Timeseries"+str(i)+".npy")
        ts2 = ts(times=two[0],values=two[1])        
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        d.append([dist,"Timeseries"+str(i)+".npy"])
        
    d.sort(key=lambda x: x[0])
    for i in range(1,n+1):
        ans.append(d[i][1])
        
    return ans


def find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius):
    """
    Given a vantage point and a radius, find the points that fall within the
    circle around the vantage point. Then calculates the distance from all of these
    points to the timeseries of interest.
    
    closest_vantage_pt: number of the vantage point being considered
    ts1: timeseries of interest
    radius: radius of circle to consider
    
    Returns: list of tuples (distance, timeseries id) in sorted order
    """
    #open database for that vantage point
    db = BinarySearchDatabase.connect("VantagePointDatabases/"+str(closest_vantage_pt)+".dbdb")
    
    #find all light curves within 2d of the vantage point
    light_curves_in_radius = db.get_nodes_less_than(radius)
    light_curves_in_radius.append(str(closest_vantage_pt)) # add in the vantage pt
    db.close()    
    
    #find similiarity between these light curves and given light curve
    distance = []
    for l in light_curves_in_radius:
        two = np.load("GeneratedTimeseries/Timeseries"+str(l)+".npy")
        ts2 = ts(times=two[0],values=two[1])
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        distance.append([dist,"Timeseries"+str(l)+".npy"]) 
    return distance

    
def find_most_similiar(filename,n, vantage_pts):
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
    given_file = np.load(filename)
    ts1 = ts(times=given_file[0],values=given_file[1])
       
    #find the most similiar vantage point = d 
    vantage_pts_dist = []
    for i in vantage_pts:
        two = np.load("GeneratedTimeseries/Timeseries"+str(i)+".npy")
        ts2 = ts(times=two[0],values=two[1])
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        vantage_pts_dist.append([dist,i])
    
    vantage_pts_dist.sort(key=lambda x: x[0])
    
    all_pts_to_check = []
    for i in range(n):
        closest_vantage_pt = vantage_pts_dist[i][1]
        radius = 2*vantage_pts_dist[i][0]
        pts_in_radius = find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius)
        for j in pts_in_radius:
            if j not in all_pts_to_check:
                all_pts_to_check.append(j)
                
    all_pts_to_check.sort(key=lambda x: x[0])
    
    for i in range(1,n+1): #ignore given timeseries 
        file_names.append(all_pts_to_check[i][1])  
        
    return file_names

def similarity_program():
    """This is a command line program that finds similiar timeseries"""
    
    print("TimeSeries Similiarity Search")
    vp = []
    with open('vp') as f:
        for line in f:
            vp.append(int(line.rstrip('\n')))
    
    keep_searching = True
    while keep_searching:
        
        #Ensure that the file given is valid
        input_var = "GeneratedTimeseries/"+input("Enter timeseries filename: ")
        while not os.path.isfile(input_var):
            input_var = input("Enter valid timeseries filename: ")
           
        #Ensure that the number of similiar filenames supplied is between 1 and 20
        flag = False
        while flag == False:
            num = input("Enter number of filenames to find: ")
            try:
                num = int(num)
                if  num <= 20 and num >= 1:
                    flag = True
                else:
                    print("Invalid number, need integer between 1 and 20")
            except ValueError:
                print("Invalid number, need integer between 1 and 20")
                
        
        print(find_most_similiar(input_var,num, vp))
    
    
        #User inputs whether to search again or end the program
        input_var = input("Search Again? (Yes/No): ")
        while input_var != 'Yes' and input_var != 'No':
            input_var = input("Search Again? (Enter Yes or No): ")
            
        if input_var == 'No':
            keep_searching = False    



if __name__ == "__main__":
    similarity_program()
        

            
    
    
    
    
       
    
    



