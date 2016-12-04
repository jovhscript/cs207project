import json
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from series import ArrayTimeSeries as ts

def encode(timeseries, filename):
    with open(filename+'.json', 'w') as outfile:
        json.dump(timeseries.__json__(), outfile, indent=4, sort_keys=True, separators=(',', ':'))

def decode(json_object):
    with open(json_object, 'r') as infile:
        d = json.load(infile)
    return ts(d['times'], d['values'])

def sdecode(json_string):
    d = json.loads(json_string)
    return ts(d['times'], d['values'])

def sencode(json_object):
    d_str = ''
    with open(json_object, 'r') as file:
        for line in file:
            d_str+=line.strip('\n')
    return d_str

