import sys
from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
from tstojson import *
import argparse
from tsdb_error import *
def fetch_byindex(ts_, n):
    s = socket(AF_INET, SOCK_STREAM)
    # s.connect(('54.164.101.248', 80))
    s.connect(('localhost', 15000))
    if n == 1:
        print("Checking the closest timeseries in the database to {}".format(ts_))
    else:
        print("Checking the {} closest timeseries in the database to {}".format(n, ts_))
    s.send("{}|{}|ind".format(ts_, str(n)).encode())
    print("Request sent to server")
    try:
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        #byte only if slicing (int otherwise)
        toget = s.recv(length).decode('utf-8')
    except:
        return 'SHIT HAPPENED'
    if kind == 'E':
        return toget
    elif kind == 'J':
        return json.loads(toget)
    else:
        return 'SHIT HAPPENED'

def fetch_upload(ts_, n):
    s = socket(AF_INET, SOCK_STREAM)
    # s.connect(('54.164.101.248', 80))
    try:
        s.connect(('localhost', 15000))
    except:
        raise TSDBConnectionError('Client socket connection failed\n')        
    if n == 1:
        print("Checking the closest timeseries in the database to {}".format(ts_))
    else:
        print("Checking the {} closest timeseries in the database to {}".format(n, ts_))
    ts_ = sencode(ts_)
    s.send("{}|{}|json".format(ts_, str(n)).encode())
    print("Request sent to server")
    try:
        received = s.recv(9)
        length = int.from_bytes(received[:8], byteorder='little')
        kind = received[8:9].decode('utf-8')
        #byte only if slicing (int otherwise)
        toget = s.recv(length).decode('utf-8')
    except:
        return 'SHIT HAPPENED (ASK RAHUL FOR THE JOKE)'
    if kind == 'E':
        return toget
    elif kind == 'J':
        return json.loads(toget)
    else:
        return 'SHIT HAPPENED (ASK RAHUL FOR THE JOKE)'

def main(arguments):
    parser = argparse.ArgumentParser(description='Finding the n most similar timeseries')
    parser.add_argument('--i', help='Index of a timeseries in the db', type=str)
    parser.add_argument('--f', help='Path to a potential json', type=str)
    parser.add_argument('--n', help='Number of neighbours', type=str, default='1')
    args = parser.parse_args(arguments)

    if args.i is not None:
        t = fetch_byindex('Timeseries'+args.i, args.n)
        print('Results:', t)
    elif args.f is not None:
        t = fetch_upload(args.f, args.n)
        print('Results:', t)
    else:
        print('ERROR: NO TIMESERIES REQUESTED.')

if __name__ == '__main__':
    # message = input('TS and N: ').split('|')
    # while message[0] != 'quit' and message[0] != 'exit':
    #     t = fetch(message[0], message[1])
    #     print('Results:', json.loads((t)))
    #     message = input('TS and N: ').split('|')
    sys.exit(main(sys.argv[1:]))
