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

user = "cs207"
password = "cs207password"
host = "localhost"
port = "5432"
db = "ts_postgres"
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

engine = create_engine(url)

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

    try:
        os.remove('ts_storagemanager.dbdb')
    except:
        pass

    print("storing imeseries into StorageManager...")
    for filename in ts_names:
        with open("GeneratedTimeseries/"+filename, 'rb') as f:
            ts_content = pickle.load(f)
            ids.append(filename[10:])
            blargs.append(np.random.uniform())
            levels.append(np.random.choice(level_choices))
            means.append(sized_ts.mean(ts_content))
            stds.append(sized_ts.std(ts_content))

            SMTimeSeries(values=ts_content._values, times=ts_content._times, id=filename[10:], dbname="ts_storagemanager.dbdb")
    print("Success!")

    genTS_df = pd.DataFrame()
    genTS_df["id"] = ids
    genTS_df["blarg"] = blargs
    genTS_df["level"] = levels
    genTS_df["mean"] = means
    genTS_df["std"] = stds

    # print("Timeseries stored into SQLite3")
    # sql_create_table="""
    # DROP TABLE IF EXISTS "ts_sqlite3";
    # CREATE TABLE "ts_sqlite3" (
    #     "id" VARCHAR PRIMARY KEY  NOT NULL ,
    #     "blarg" FLOAT(16) NOT NULL,
    #     "level" CHAR(1) NOT NULL,
    #     "mean" FLOAT(16) NOT NULL,
    #     "std" FLOAT(16) NOT NULL
    # );
    # """
    # PATHSTART="."
    # def get_db(dbfile):
    #     sqlite_db = sq3.connect(os.path.join(PATHSTART, dbfile))
    #     return sqlite_db
    #
    # def init_db(dbfile, schema):
    #     """Creates the database tables."""
    #     db = get_db(dbfile)
    #     db.cursor().executescript(schema)
    #     db.commit()
    #     return db
    #
    # # EXECUTE OURSCHEMA TO CREATE TS_SQLITE3.DB
    # db=init_db("ts_sqlite3.db", sql_create_table)
    #
    #
    # # INSERT genTS_df TO THE DATABASE
    # genTS_df.to_sql("ts_sqlite3", db, if_exists="replace", index=False)
    # print("Success")

    print("Timeseries stored into PostGres")
    genTS_df.to_sql("ts_postgres", engine, if_exists="replace")
    print("Success!")


storeGenTS(engine=engine)

print("testcase: querying the first ts and its metadata: ")
test_ts = SMTimeSeries().from_db(id="1", dbname="ts_storagemanager.dbdb")
print("from storagemanager", test_ts)

query = """SELECT * FROM ts_postgres WHERE id='1';"""
with engine.connect() as conn:
    result = conn.execute(query)
    print("from postgres", result.fetchall())
