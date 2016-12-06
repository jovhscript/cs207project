from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
import threading

from BinarySearchDatabase import *
import find_most_similiar
from tstojson import *
with open('VantagePointDatabases/vp') as f:
    vp = []
    for line in f:
        vp.append(int(line.rstrip('\n'))) 

def db_client(sock, client_addr):
    global vp
    print('Got connection from', client_addr) 
    while True:
        msg = sock.recv(65536)
        print("msg", msg)
        if not msg:
            break
        ts_interest, n = msg.decode().split('/')
        try:
            ts_interest = sdecode(ts_interest)
            js = True
        except:
            js = False
        print("ts: {}, n closest: {}".format(ts_interest, n))
        if js:
            tss_to_return = find_most_similiar.find_most_similiar(ts_interest, int(n), vp, False)
        else:
            tss_to_return = find_most_similiar.find_most_similiar("GeneratedTimeseries/"+ts_interest, int(n), vp)
        print(tss_to_return)
        sock.sendall(json.dumps(tss_to_return).encode())
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

launch()
