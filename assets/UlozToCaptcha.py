# -*- coding: utf-8 -*-
import struct
import os
from ...common.json_layer import json
from ..internal.Addon import Addon
import socket
from ...common.json_layer import json

class UlozToCaptcha(Addon):
    __name__ = "UlozToCaptcha"
    __type__ = "hook"
    __version__ = "0.3"
    __status__ = "testing"

    __config__ = [("activated", "bool", "Activated", True),
                  ("host", "string", "IP or hostname or localhost", "pyload.xxx"),
                  ("port", "int", "Port of open socket", 9988)]

    __description__ = """Solve captcha by tensor"""
    __license__ = "GPLv3"
    __authors__ = [("Jdvorak23", "dvorakj3@post.cz")]


    def captcha_task(self, task):
        if task.captchaParams['plugin'] is not 'UlozTo':
            return False
        self.log_info("UlozTo captcha solver - local");
        task.handler.append(self)
        task.data['service'] = self.classname
        task.setWaiting(2300)
               
        result = self.send_json(task.getCaptcha())

        self.log_info("Captcha result: " + result)
        task.data['captchaResult'] = result
        task.setResult(result)

    def captcha_invalid(self, task):
        if task.data['service'] == self.classname and "captchaResult" in task.data:
            self.log_info("Wrong captcha: " + task.data['captchaResult']);
            try:
                data = {}
                data['wrong'] = task.data['captchaResult']
                self.send_json([data])
                self.log_info("Wrong captcha sent to server: " + task.data['captchaResult']);
            except OSError:
                pass
    def send_json(self, obj):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((self.config.get('host'), self.config.get('port')))
        msg = json.dumps(obj).encode()
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        mySocket.sendall(msg)
        data = mySocket.recv(1024)
        mySocket.close()
        return data.decode()
