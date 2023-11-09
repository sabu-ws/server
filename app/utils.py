from datetime import datetime
import os
import subprocess


def logging(action, message):
    file = open(f"{LOG_PATH}/gui.log", "a")
    date_format = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    prefetch = f"{date_format} [GUI][{str(action)}] {message}\n"
    file.write(prefetch)
    file.close()

def getHostname():
    return subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")

def setHostname(hostname):
    subprocess.Popen(["hostnamectl","set-hostname",str(hostname)])
    
    return ""

def getInterface():
    return ""