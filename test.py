import subprocess

env = {'IMAGE_PATH': 'images/good.jpg'}

proc = subprocess.Popen("python3 captcha.py", shell=True, stdout=subprocess.PIPE, env=env)
result = proc.communicate()[0].rstrip()

print(result)
