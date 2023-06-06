# -*- coding: utf-8 -*-

import subprocess
import os
from ...common.json_layer import json
from ..internal.Addon import Addon


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
        task.setWaiting(5000)

        image = task.captchaParams['file']
        with open(self.config.get('folder') + "captcha.txt", "w") as text_file:
            text_file.write(os.getcwd() + "/" + image)

        proc = subprocess.Popen(self.config.get('python3') + " " + self.config.get('folder') + "captcha.py", shell=True, stdout=subprocess.PIPE)
        result = proc.communicate()[0].rstrip()
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



