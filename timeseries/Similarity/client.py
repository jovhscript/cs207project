import sys
from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
from tstojson import *
def fetch(ts_, n):
    s = socket(AF_INET, SOCK_STREAM)
    # s.connect(('54.164.101.248', 80))
    s.connect(('localhost', 15000))
    if n == 1:
        print("Checking the closest timeseries in the database to {}".format(ts_))
    else:
        print("Checking the {} closest timeseries in the database to {}".format(n, ts_))
    try:
        ts_ = sencode(ts_)
    except:
        pass
    s.send("{}/{}".format(ts_, str(n)).encode())
    print("Request sent to server")
    return json.loads(s.recv(65536).decode())

# pool = ThreadPoolExecutor(20)
# thrs=[]
# message = input('TS and N: ').split('/')
# while message[0] != 'quit' and message[0] != 'exit':
# # while True:
#     t = fetch(message[0], message[1])
#     print('Results:', json.loads((t)))
#     message = input('TS and N: ').split('/')