from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
import threading

from BinarySearchDatabase import *
import find_most_similiar
from tstojson import *
from tsdb_error import *

with open('VantagePointDatabases/vp') as f:
    vp = []
    for line in f:
        vp.append(int(line.rstrip('\n'))) 

def db_client(sock, client_addr):
    global vp
    print('Got connection from', client_addr) 
    while True:
        msg = sock.recv(65536)
        # print("msg", msg)
        if not msg:
            error = 'ERROR 400: SERVER CONNECTION FAILED'.encode('utf-8')
            tosend = (len(error)).to_bytes(8, byteorder='little')+'E'.encode('utf-8')+error
            sock.sendall(tosend)
            sock.close()
            raise TSDBConnectionError('Client socket connection failed\n')

        ts_interest, n, typ = msg.decode().split('|')
        if typ == 'json':
            ts_interest = sdecode(ts_interest)
            js = True
        else:
            js = False
        # print("ts: {}, n closest: {}".format(ts_interest, n))
        if js:
            tss_to_return = find_most_similiar.find_most_similiar(ts_interest, int(n), vp, False)
        else:
            tss_to_return = find_most_similiar.find_most_similiar("GeneratedTimeseries/"+ts_interest, int(n), vp)
        
        if isinstance(tss_to_return, str):
            print ('Error', tss_to_return)
            if 'INDEX' in tss_to_return:
                error = 'ERROR 400: NO SUCH INDEX IN DATABASE'.encode('utf-8')
            elif 'NUMBER' in tss_to_return:
                error = 'ERROR 400: N should be between 1 and {}'.format(tss_to_return.split(' | ')[1]).encode('utf-8')
            elif 'TYPE' in tss_to_return:
                error = 'ERROR 400: input must be a time series'.encode('utf-8')

            tosend = (len(error)).to_bytes(8, byteorder='little')+'E'.encode('utf-8')+error
            sock.sendall(tosend)
            sock.close()

        for t in tss_to_return:
            t.append(pickle.load(open("GeneratedTimeseries/"+t[1], 'rb')).__json__())

        if js:
            tss_to_return.insert(0, [0, 'itself', ts_interest.__json__()])

        jsonencoded = json.dumps(tss_to_return).encode('utf-8')
        tosend = (len(jsonencoded)).to_bytes(8, byteorder='little')+'J'.encode('utf-8')+jsonencoded
        sock.sendall(tosend)
    print('Client closed connection') 
    sock.close()

def db_server(addr):
    print("Server Started...")
    pool = ThreadPoolExecutor(50) 
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(15)
    while True:
        print('connection')
        client_sock, client_addr = sock.accept()
        pool.submit(db_client, client_sock, client_addr)
        
# db_server(('172.31.53.79', 80))
def launch():
    db_server(('', 15000))

if __name__ == '__main__':
    launch()

