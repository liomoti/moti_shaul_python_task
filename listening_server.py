import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 2020

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))

ServerSocket.close()