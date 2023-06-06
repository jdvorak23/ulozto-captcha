import socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(("localhost", 9988))
mySocket.send('/var/www/ulozto-captcha/images/good.jpg'.encode())
data = mySocket.recv(1024)
mySocket.close()
print(data.decode())