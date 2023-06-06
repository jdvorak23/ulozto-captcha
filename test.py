# -*- coding: utf-8 -*-
import socket
import json
import base64
import pathlib
import struct

PORT = 9988

path = str(pathlib.Path(__file__).parent.resolve())

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

IP = get_ip()
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