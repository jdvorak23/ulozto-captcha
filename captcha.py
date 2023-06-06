
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import PIL
import pathlib
import os
import socket

path = str(pathlib.Path(__file__).parent.resolve())
interpreter = tflite.Interpreter(model_path = path + "/model.tflite")

def solve_captcha(imagePath):
    print(imagePath)
    image = Image.open(imagePath)
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


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(("localhost", 9988))
mySocket.listen(1)

while True:
    client, addr = mySocket.accept()
    data = client.recv(1024)
    captcha = solve_captcha(data.decode())
    client.send(captcha.encode())
    client.close()
