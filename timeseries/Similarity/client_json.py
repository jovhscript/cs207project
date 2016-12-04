import sys
from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
from tstojson import *
def fetch(ts_json, n):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 15000))
    if n == 1:
        print("Checking the closest timeseries in the database to {}".format(ts_json))
    else:
        print("Checking the {} closest timeseries in the database to {}".format(n, ts_json))
    ts_str = sencode(ts_json)
    s.send("{}/{}".format(ts_str, str(n)).encode())
    print("Request sent to server")
    return s.recv(65536)

pool = ThreadPoolExecutor(20)
thrs=[]
message = input('TS and N: ').split('/')
while message[0] != 'quit' and message[0] != 'exit':
# while True:
    t = pool.submit(fetch, message[0], message[1])
    thrs.append(t)
    print('Results:', str(thrs[-1].result().decode()))
    message = input('TS and N: ').split(' ')