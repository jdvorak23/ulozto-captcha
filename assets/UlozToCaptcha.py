# -*- coding: utf-8 -*-

import subprocess
import os
from ...common.json_layer import json
from module.network.RequestFactory import getRequest as get_request
from ..internal.Addon import Addon


class UlozToCaptcha(Addon):
    __name__ = "UlozToCaptcha"
    __type__ = "hook"
    __version__ = "0.1"
    __status__ = "testing"

    __config__ = [("activated", "bool", "Activated", True),
                  ("submitUrl", "string", "Url for solving captcha", "http://ulozto-captcha.xxx/captcha"),
                  ("wrongCaptchaUrl", "string", "Url to say wrong captcha", "http://ulozto-captcha.xxx/wrong-captcha")]

    __description__ = """Solve captcha by tensor"""
    __license__ = "GPLv3"
    __authors__ = [("Jdvorak23", "dvorakj3@post.cz")]


    def captcha_task(self, task):
        if task.captchaParams['plugin'] is not 'UlozTo':
            return False
        self.log_debug("UlozTo captcha solver");
        task.handler.append(self)
        task.data['service'] = self.classname
        task.setWaiting(100)
        res = self.load(
            self.config.get('submitUrl'), 
            post=json.dumps(task.getCaptcha())
            )
        self.log_debug(res)
        result = res.strip()
        self.log_debug("Captcha result: " + result)
        task.data['captchaResult'] = result
        task.setResult(result)
        
    def captcha_invalid(self, task):
        self.log_debug("Wrong captcha")
        if task.data['service'] == self.classname and "captchaResult" in task.data:
            res = self.load(
                self.config.get('wrongCaptchaUrl'), 
                post=json.dumps([task.data['captchaResult']])
                )
            self.log_debug(res)


