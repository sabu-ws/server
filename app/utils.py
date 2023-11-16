from datetime import datetime
import os
import subprocess
from pyroute2 import NDB, IPRoute
from socket import AF_INET
from dataclasses import dataclass

@dataclass
class network:
    interface: str
    ip: str
    netmask: str
    gateway: str


ndb = NDB()

def logging(action, message):
    file = open(f"{LOG_PATH}/gui.log", "a")
    date_format = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    prefetch = f"{date_format} [GUI][{str(action)}] {message}\n"
    file.write(prefetch)
    file.close()


def getHostname():
    return (
        subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        .communicate()[0]
        .decode()
        .replace("\n", "")
    )


def list_interfaces():
    with IPRoute() as ipr:
        return [x.get_attr('IFLA_IFNAME') for x in ipr.get_links() if x.get_attr('IFLA_IFNAME') != "lo"]


def get_IP_Server(interfaces="enp0s3"):
    return tuple(ndb.interfaces[interfaces].ipaddr.summary()[0])[3]
