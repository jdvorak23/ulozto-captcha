# -*- coding: utf-8 -*-
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import pathlib
import socket
import base64
import json
from io import BytesIO
import re
import os
import struct

PORT = 9988
IP = "localhost"

path = str(pathlib.Path(__file__).parent.resolve())
interpreter = tflite.Interpreter(model_path = path + "/model.tflite")

def solve_captcha(image):
    img = np.asarray(image)
    img = (img / 255).astype(np.float32)

    # convert to grayscale
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    input = 0.299 * r + 0.587 * g + 0.114 * b

    # input has nowof  shape (70, 175)
    # we modify dimensions to match model's input
    input = np.expand_dims(input, 0)
    input = np.expand_dims(input, -1)
    # input is now of shape (batch_size, 70, 175, 1)
    # output will have shape (batch_size, 4, 26)


    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input)
    interpreter.invoke()

    # predict and get the output
    output = interpreter.get_tensor(output_details[0]['index'])
    # now get labels
    labels_indices = np.argmax(output, axis=2)

    available_chars = "abcdefghijklmnopqrstuvwxyz"

    def decode(li):
        result = []
        for char in li:
            result.append(available_chars[char])
        return "".join(result)

    decoded_label = [decode(x) for x in labels_indices][0]

    image.save(path + "/images/" + decoded_label + ".jpg")

    return decoded_label

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

print("IP: " + IP + "\nPort: " + str(PORT))

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((IP, PORT))
mySocket.listen(1)

while True:
    client, addr = mySocket.accept()
    result = ""
    try:
        data = recv_msg(client)
        json_data = json.loads(data.decode())

        if "src" in json_data[0]:
            image_data = re.sub('^data:image/.+;base64,', '', json_data[0]['src'])
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            result = solve_captcha(image)
            print("Captcha resolved: " + result)
        if "wrong" in json_data[0]:
            imagePath = path + "/images/" + json_data[0]['wrong'] + ".jpg"
            os.remove(imagePath)
            print("Wrong solved captcha image removed: " + json_data[0]['wrong'] + ".jpg");
    except Exception as e:
        print(e)
    finally:
        client.send(result.encode())
        client.close()
