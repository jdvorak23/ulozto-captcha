# -*- coding: utf-8 -*-

import os
from ...common.json_layer import json
from ..internal.Addon import Addon
import socket
from ...common.json_layer import json

class UlozToCaptcha(Addon):
    __name__ = "UlozToCaptcha"
    __type__ = "hook"
    __version__ = "0.2"
    __status__ = "testing"

    __config__ = [("activated", "bool", "Activated", True),
                  ("folder", "string", "Directory with captcha resolver", "/root/ulozto-captcha/"),
                  ("host", "string", "IP or hostname or localhost", "pyload.xxx"),
                  ("port", "string", "Port of open socket", "9988")]

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
               
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect((self.config.get('host'), self.config.get('port')))

        mySocket.send(json.dumps(task.getCaptcha()).encode())
        data = mySocket.recv(1024)
        mySocket.close()
        result = data.decode()

        self.log_info("Captcha result: " + result)
        task.data['captchaResult'] = result
        task.setResult(result)

    def captcha_invalid(self, task):
        if task.data['service'] == self.classname and "captchaResult" in task.data:
            self.log_info("Wrong captcha: " + task.data['captchaResult']);
            try:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mySocket.connect((self.config.get('host'), self.config.get('port')))
                data = {}
                data['wrong'] = task.data['captchaResult']
                mySocket.send(json.dumps([data]).encode())
                mySocket.close()
                self.log_info("Wrong captcha sent to server: " + task.data['captchaResult']);
            except OSError:
                pass



