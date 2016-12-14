import os, sys
import pickle
sys.path.append("../")
from interfaces import SizedContainerTimeSeriesInterface as sized_ts
from series import SMTimeSeries
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from random import shuffle
from sqlite3 import dbapi2 as sq3

### This script creates the StorageManager and PostGreSQL database used for the app

def storeGenTS(engine):
    ### Fetch all the file names
    ts_names = os.listdir("GeneratedTimeseries")
    shuffle(ts_names)   ### Random shuffling the order each timeseries is stored, so that the binary search tree for storage manager is balanced
    ### Initialize the lists of values to be stored in postgres
    level_choices = ["A", "B", "C", "D", "E", "F"]
    ids = []
    blargs = []
    levels = []
    means = []
    stds = []

    # remove the StorageManager if it exists
    try:
        os.remove('ts_storagemanager.dbdb')
    except:
        pass

    print("storing imeseries into StorageManager...")
    for filename in ts_names:
        with open("GeneratedTimeseries/"+filename, 'rb') as f:
            ts_content = pickle.load(f)
            # calculate the metadata and append it to list
            ids.append(filename[10:])
            blargs.append(np.random.uniform())
            levels.append(np.random.choice(level_choices))
            means.append(sized_ts.mean(ts_content))
            stds.append(sized_ts.std(ts_content))

            # store each timeseries into StorageManager
            SMTimeSeries(values=ts_content._values, times=ts_content._times, id=filename[10:], dbname="ts_storagemanager.dbdb")
    print("Success!")

    # make a dataframe for MetaData
    genTS_df = pd.DataFrame()
    genTS_df["id"] = ids
    genTS_df["blarg"] = blargs
    genTS_df["level"] = levels
    genTS_df["mean"] = means
    genTS_df["std"] = stds

    print("Timeseries stored into PostGres")
    # store the metadata into PostGreSQL database with to_sql
    genTS_df.to_sql("ts_postgresql", engine, if_exists="replace")
    print("Success!")

if __name__ == '__main__':
    # set up db configuration for postgresql and the engine
    user = "cs207"
    password = "cs207password"
    host = "localhost"
    port = "5432"
    db = "ts_postgres"
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url)

    storeGenTS(engine=engine)