# -*- coding: utf-8 -*-
import socket
import json
import base64
import pathlib

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
IP = get_ip()
print("IP: " + IP + "\nPort: " + PORT)

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(IP, 9988)

data = {}
with open(path + "/images/good.jpg", mode='rb') as file:
    img = file.read()

data['src'] = base64.encodebytes(img).decode("utf-8")

json_data = json.dumps([data])

mySocket.send(json_data.encode())
data = mySocket.recv(65536)
mySocket.close()
print(data.decode())