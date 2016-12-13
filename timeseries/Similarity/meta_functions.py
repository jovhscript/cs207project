import os, sys
import pickle
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from interfaces import SizedContainerTimeSeriesInterface as sized_ts
from series import SMTimeSeries
import numpy as np
import pandas as pd
import json
from sqlalchemy import create_engine


# set up db configuration
user = "cs207"
password = "cs207password"
host = "localhost"
port = "5432"
db = "ts_postgres"
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
engine = create_engine(url)

def _make_query(engine, query):
    with engine.connect() as conn:
        res = conn.execute(query)
    return res

def meta_get(engine):
    """
    return metadata for all timeseries
    """
    out = _make_query(engine, """SELECT * FROM ts_postgresql ORDER BY CAST(id AS int)""")
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    return [out_col, out_rec]

def meta_filter(engine, filter_input):
    """
    return metadata based on the filter
    """
    ls, ms, stds = filter_input
    if ls != "":
        clause_where = "WHERE level IN {}".format(tuple(set(ls)))
    elif ms is not None:
        clause_where = "WHERE mean >= {} AND mean <= {}".format(ms[0], ms[1])
    elif stds is not None:
        clause_where = "WHERE std >= {} AND std <= {}".format(stds[0], stds[1])

    query = "SELECT * FROM ts_postgresql {} ORDER BY CAST(id AS int)".format(clause_where)
    print(query)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    return [out_col, out_rec]

def meta_id(engine, request_id):
    """
    return metadata and timeseries by id
    """
    query = "SELECT * FROM ts_postgresql WHERE id='{}'".format(request_id)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    ts = SMTimeSeries().from_db(id=request_id, dbname="ts_storagemanager.dbdb")
    return [out_col, [list(x) for x in out_rec], ts._times, ts._values]

def meta_post(engine, filename):
    """
    insert new timeseries into StorageManager and Metadata, and return timeseries
    Parameters:
    - jsonfile needs to be in the format of:
    {
    "id": id,
    "ts": timeseries containing "times" and "values" as keys to lists
    }
    """
    with open(filename) as data_file:
        data = json.load(data_file)

    id_new = data["id"]
    ts = data["ts"]

    try:
        SMTimeSeries().from_db(id=id_new, dbname="ts_storagemanager.dbdb")
        raise KeyError("ERROR: id already exist in database")
    except:
        pass

    ### inserting
    ts_new = SMTimeSeries(times=ts["times"], values=ts["values"], id=id_new, dbname="ts_storagemanager.dbdb").ts
    print("New timeseries successfully stored into StorageManager")
    mean_new = sized_ts.mean(ts_new)
    std_new = sized_ts.std(ts_new)
    query = "INSERT INTO ts_postgresql (id, blarg, level, mean, std) VALUES ('{}', {}, Null , Null , {})".format(id_new, mean_new, std_new)
    out = _make_query(engine, query)
    print("New metadata successfully stored into PostgreSQL")

    ### quering the newly-inserted
    query = "SELECT * FROM ts_postgresql WHERE id='{}'".format(id_new)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    return [out_col, [list(x) for x in out_rec], ts_new._times, ts_new._values]

if __name__ == '__main__':
    ### create a json uploadable for testing meta_post():
    test_dict = {"id": 1001,
                 "ts": {
                        "times": [1, 2, 3, 4, 5],
                        "values": [0.98, 0.99, 1, 0.99, 0.98]
        }}

    with open("Timeseries1001.json", 'w') as fp:
        json.dump(test_dict, fp)

    meta_post(engine, 'Timeseries1001.json')
    print(meta_id(engine, 1001))
