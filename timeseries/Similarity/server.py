from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
from concurrent.futures import ThreadPoolExecutor
import threading

from BinarySearchDatabase import *
import find_most_similiar

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
        ts_name, n = msg.decode().split(' ')
        print("ts: {}, n closest: {}".format(ts_name, n))
        print(vp)
        tss = find_most_similiar.find_most_similiar("GeneratedTimeseries/"+ts_name, int(n), vp)
        print(tss)
        sock.sendall(str(tss).encode())
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
        
db_server(('',15000))