import subprocess
import time
while True:
    p = subprocess.Popen(['python', 'main.py'])
    time.sleep(300)
    p.kill()
