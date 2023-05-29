#import socket module
from socket import *
import threading

def server(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode() #Fill in start #Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read() #Fill in start #Fill in end
        #Send one HTTP header line into socket
        #Fill in start
        header = "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(header.encode()) #must be in bytes
        #Fill in end
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        #Send response message forfile not found
        #Fill in start
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Fill in end
    #Close client socket
    #Fill in start
    connectionSocket.close()
    #Fill in end

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverPort = 80
serverSocket.bind(('', serverPort))
serverSocket.listen(10) #harus lebih dari 1, agar bisa menerima lebih dari 1 request dan multithread bisa berguna
#Fill in end

print('Ready to serve...')
while True:
    #Establish the connection
    connectionSocket, addr = serverSocket.accept() #Fill in start #Fillin end
    t = threading.Thread(target=server, args=(connectionSocket, addr))
    t.start()