import subprocess

env = {'IMAGE_PATH': 'images/good.jpg'}

proc = subprocess.Popen("/root/.pyenv/versions/3.9.16/bin/python captcha.py", shell=True, stdout=subprocess.PIPE, env=env)
result = proc.communicate()[0].rstrip()

print(result)
