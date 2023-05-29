import socket
import sys

host = '10.60.229.210' #127.0.0.1
dataPayload = 1024 #1 kb = 1024 karakter

def startClient(port):
    sock = socket.socket()
    serverAddr = (host, port)
    print('Client\n=======\n')
    print('Terhubung ke server :', serverAddr)
    sock.connect(serverAddr)

    while True:
        try:
            message = input('client : ')
            if message == 'exit' :
                sock.send(b'client keluar')
                sock.close()
                break
            sock.send(message.encode('utf-8')) #mengirim ke server
            data = sock.recv(dataPayload) #menerima pesan dari server
            if data:
                print('server : %s' % data.decode('utf-8'))
        except:
            print('error')
            sock.close()
            break
startClient(5000)