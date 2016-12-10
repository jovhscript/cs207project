import json
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from series import ArrayTimeSeries as ts
from tsdb_error import *

def encode(timeseries, filename):
    with open(filename+'.json', 'w') as outfile:
        json.dump(timeseries.__json__(), outfile, indent=4, sort_keys=True, separators=(',', ':'))

def decode(json_object):
    with open(json_object, 'r') as infile:
        try:
            d = json.load(infile)
            return ts(d['times'], d['values'])
        except json.JSONDecodeError:
            raise TSDBInputError('Invalid JSON object received\n')
            #return None

def sdecode(json_string):
    try:
        d = json.loads(json_string)
        return ts(d['times'], d['values'])
    except json.JSONDecodeError:
        raise TSDBInputError('Invalid JSON object received:\n'+str(json_str))
        #return None


def sencode(json_object):
    d_str = ''
    with open(json_object, 'r') as file:
        for line in file:
            d_str+=line.strip('\n')
    return d_str

