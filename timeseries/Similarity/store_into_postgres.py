import os, sys
import pickle
sys.path.append("../")
from interfaces import SizedContainerTimeSeriesInterface as sized_ts
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

ts_names = os.listdir("GeneratedTimeseries")
level_choices = ["A", "B", "C", "D", "E", "F"]
ids = []
blargs = []
levels = []
means = []
stds = []

for filename in ts_names:
    with open("GeneratedTimeseries/"+filename, 'rb') as f:
        ts_content = pickle.load(f)
        ids.append(filename[10:])
        blargs.append(np.random.uniform())
        levels.append(np.random.choice(level_choices))
        means.append(sized_ts.mean(ts_content))
        stds.append(sized_ts.std(ts_content))

genTS_df = pd.DataFrame()
genTS_df["id"] = ids
genTS_df["blarg"] = blargs
genTS_df["level"] = levels
genTS_df["mean"] = means
genTS_df["std"] = stds

user = "cs207"
password = "cs207password"
host = "localhost"
port = "5432"
db = "ts_postgres"
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

engine = create_engine(url)
genTS_df.to_sql("generated_timeseries", engine, if_exists="replace")