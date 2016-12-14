import os, sys
import pickle
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from interfaces import SizedContainerTimeSeriesInterface as sized_ts
from series import SMTimeSeries
import json
from sqlalchemy import create_engine

### This file supports myapp.py with functions that get, post and filter metadata and timeseries

# set up db configuration for postgresql and the engine
user = "cs207"
password = "cs207password"
host = "localhost"
port = "5432"
db = "ts_postgres"
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
engine = create_engine(url)

def _make_query(engine, query):
    """
    Helper function that execute a query in the postgresql database

    Parameter:
    -------
    engine: a postgresql engine
    query: a string representation of a SQL query operated on a table in the database

    Returns:
    -------
    res: the output object of the query, to which multiple methods/attributes could be applied
    """
    with engine.connect() as conn:
        res = conn.execute(query)
    return res

def meta_get(engine):
    """
    return metadata for all timeseries

    Parameter:
    -------
    engine: a postgresql engine

    Returns:
    -------
    a jasonifiable structure with [[col1, col2, ...coln],
                                   [(val01, val02, ..., val0n),
                                    (val11, val12, ..., val1n),
                                    ...]]
    """
    out = _make_query(engine, """SELECT * FROM ts_postgresql ORDER BY CAST(id AS int)""") # order records by the id
    out_rec = out.fetchall()
    out_col = out._metadata.keys ### grab the column names
    return [out_col, out_rec]

def meta_filter(engine, filter_input):
    """
    return metadata based on the filter

    Parameter:
    -------
    engine: a postgresql engine
    filter: a list of the filter variables: [levels, means, stds]
        - only one of the three variables will be non-empty:
        - levels: list of level characters: ["A", "B", "E"], empty string "" if None
        - means: list of min and max means: [0.999, 1.001], None if None
        - stds: list of min and max means: [0.96, 1], None if None
    Returns:
    -------
    a jasonifiable structure with [[col1, col2, ...coln],
                                   [(val01, val02, ..., val0n),
                                    (val11, val12, ..., val1n),
                                    ...]]
    """
    ls, ms, stds = filter_input
    if ls != "":
        clause_where = "WHERE level IN {}".format(tuple(set(ls))) # creating a where statement to filter the result
    elif ms is not None:
        clause_where = "WHERE mean >= {} AND mean <= {}".format(ms[0], ms[1])
    elif stds is not None:
        clause_where = "WHERE std >= {} AND std <= {}".format(stds[0], stds[1])

    query = "SELECT * FROM ts_postgresql {} ORDER BY CAST(id AS int)".format(clause_where) #dynamically add "where" to query
    # print(query)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    return [out_col, out_rec]

def meta_id(engine, request_id):
    """
    return metadata and timeseries by id

    Parameter:
    -------
    id: non-negative integer

    Returns:
    -------
    a jasonifiable structure with [[column names], [list of [records]], [_times], [_values]]
    """
    if (request_id<0) or (not isinstance(request_id, int)): # the id has to be non-negative integer
        return "ERROR | id has to be a non-negative integer"
    query = "SELECT * FROM ts_postgresql WHERE id='{}'".format(request_id)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    ts = SMTimeSeries().from_db(id=request_id, dbname="ts_storagemanager.dbdb") # extract the timeseries from StorageManager
    return [out_col, [list(x) for x in out_rec], ts._times, ts._values]

def meta_post(engine, filename):
    """
    insert new timeseries into StorageManager and Metadata, and return timeseries

    Parameters:
    ------------
    - jsonfile needs to be in the format of:
    {
    "id": id,
    "ts": timeseries containing "times" and "values" as keys to lists
    }

    Returns:
    -------
    a jasonifiable structure with [[column names], [list of [records]], [_times], [_values]]
    """
    # load the json time series with id
    try:
        with open(filename) as data_file:
            data = json.load(data_file)
    except:
        return "ERROR | JSON has incorrect filename or is corrupt"
    try:
        id_new = data["id"]
        ts = data["ts"]
        ts_times = ts["times"]
        ts_values = ts["values"]
    except:
        return "ERROR | uploaded JSON's format is not valid"

    # check if id is already in the database (StorageManager)
    try:
        SMTimeSeries().from_db(id=id_new, dbname="ts_storagemanager.dbdb")
        return "ERROR | id already exist in database"
    except:
        pass

    # inserting
    #   to StorageManager
    try:
        ts_new = SMTimeSeries(times=ts["times"], values=ts["values"], id=id_new, dbname="ts_storagemanager.dbdb").ts
    except:
        return "ERROR | input timeseries is not valid"
    print("New timeseries successfully stored into StorageManager")
    #   to PostGreSQL
    mean_new = sized_ts.mean(ts_new) # calculate new mean
    std_new = sized_ts.std(ts_new) # calculate new std
    query = "INSERT INTO ts_postgresql (id, blarg, level, mean, std) VALUES ('{}', {}, Null , Null , {})".format(id_new, mean_new, std_new)
    _make_query(engine, query) ### excute query to insert into SQL database
    print("New metadata successfully stored into PostgreSQL")

    # quering the newly-inserted and return the result for rendering
    query = "SELECT * FROM ts_postgresql WHERE id='{}'".format(id_new)
    out = _make_query(engine, query)
    out_rec = out.fetchall()
    out_col = out._metadata.keys
    return [out_col, [list(x) for x in out_rec], ts_new._times, ts_new._values]

# generate the test_case
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
