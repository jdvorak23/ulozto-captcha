# -*- coding: utf-8 -*-

import subprocess
import os
from ...common.json_layer import json
from ..internal.Addon import Addon
import socket


class UlozToCaptcha(Addon):
    __name__ = "UlozToCaptcha"
    __type__ = "hook"
    __version__ = "0.2"
    __status__ = "testing"

    __config__ = [("activated", "bool", "Activated", True),
                  ("folder", "string", "Directory with captcha resolver", "/root/ulozto-captcha/"),
                  ("python3", "string", "Exact python3 interpreter which has all dependencies installed", "/root/.pyenv/versions/3.9.16/bin/python")]

    __description__ = """Solve captcha by tensor"""
    __license__ = "GPLv3"
    __authors__ = [("Jdvorak23", "dvorakj3@post.cz")]


    def captcha_task(self, task):
        if task.captchaParams['plugin'] is not 'UlozTo':
            return False
        self.log_info("UlozTo captcha solver - local");
        task.handler.append(self)
        task.data['service'] = self.classname

        imagePath = os.getcwd() + "/" + task.captchaParams['file']
               
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.connect(("localhost", 9988))
        mySocket.send(imagePath.encode())
        data = mySocket.recv(1024)
        mySocket.close()
        result = data.decode()
        
        task.setWaiting(5000)
        self.log_info("Captcha result: " + result)
        task.data['captchaResult'] = result
        task.setResult(result)

    def captcha_invalid(self, task):
        self.log_info("Wrong captcha");
        if task.data['service'] == self.classname and "captchaResult" in task.data:
            try:
                file = self.config.get('folder') + "images/" + task.data['captchaResult'] + ".jpg"
                os.remove(file)
                self.log_info("Wrong captcha image removed: " + file);
            except OSError:
                pass



