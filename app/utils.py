import os
import subprocess
from datetime import datetime
from config import *


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def getHostname():
    return os.popen("hostname").read()

# def getNetInfo(box):
#     info_ip = subprocess.Popen(f"{SCRIPT_PATH}/network/network-read.sh".split(),stdout=subprocess.PIPE).communicate()[0].decode().split("\n")
#     net_dico = {
#         "interface":info_ip[0],
#         "ip":info_ip[1],
#         "netmask":info_ip[2],
#         "gateway":info_ip[3],
#         "dns1":info_ip[4],
#         "dns2":info_ip[5],
#     }
#     if box not in net_dico:
#         return None
#     return net_dico[box]

def logging(action,message):
    file = open(f"{LOG_PATH}/gui.log","a")
    date_format = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    prefetch = f"{date_format} [GUI][{str(action)}] {message}\n"
    file.write(prefetch)
    file.close()