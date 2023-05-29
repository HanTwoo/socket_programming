import socket
import sys

host = '10.60.229.210' #127.0.0.1
dataPayload = 1024 #1 kb = 1024 karakter
retry = 1

def startServer(port):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverAddr = (host, port)
    print('SERVER\n=======\n')
    print('Menjalankan server :', serverAddr)
    
    sock.bind(serverAddr)
    sock.listen(retry)
    client, address = sock.accept()


    print('Terhubung dengan client', address)
    while True:
        data = client.recv(dataPayload)
        if data:
            print("client : %s" % data.decode('utf-8'))
            balas = input('server :')
            if balas == 'exit':
                client.send(b'keluar')
                client.close()
                break
            client.send(balas.encode('utf-8'))
startServer(5000)
