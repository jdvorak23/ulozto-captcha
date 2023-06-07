# -*- coding: utf-8 -*-
import socket
import json
import base64
import pathlib
import struct

PORT = 9988
IP = "localhost"

path = str(pathlib.Path(__file__).parent.resolve())

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

print("IP: " + IP + "\nPort: " + str(PORT))

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect((IP, PORT))

data = {}
with open(path + "/images/good.jpg", mode='rb') as file:
    img = file.read()

data['src'] = base64.encodebytes(img).decode("utf-8")

json_data = json.dumps([data])
send_msg(mySocket, json_data.encode())
data = mySocket.recv(1024)
mySocket.close()
print(data.decode())