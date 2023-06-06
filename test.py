# -*- coding: utf-8 -*-
import socket
import json
import base64

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(("192.168.1.223", 9988))

data = {}
with open("/root/ulozto-captcha/images/good.jpg", mode='rb') as file:
    img = file.read()

data['src'] = base64.encodebytes(img).decode("utf-8")

json_data = json.dumps([data])

mySocket.send(json_data.encode())
data = mySocket.recv(65536)
mySocket.close()
print(data.decode())