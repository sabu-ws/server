from config import *

from sqlalchemy import URL

from pyroute2 import NDB, IPRoute
from socket import AF_INET
from dataclasses import dataclass
from datetime import datetime
import os
import subprocess

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
    interfaces = list_interfaces()
    ip = ""
    for interface in interfaces:
        if tuple(ndb.interfaces[interface].ipaddr.summary()) != ():
            return tuple(tuple(ndb.interfaces[interface].ipaddr.summary())[0])[3]

def database_allowed():
    if str(DB_PROTOCOLE) in ["sqlite"]:
        return URL.create(
            DB_PROTOCOLE,
            database=DB_NAME,
        )
    elif str(DB_PROTOCOLE) in ["postgresql","postgresql+psycopg2","postgresql+pg8000","mysql","mysql+mysqldb","mysql+pymysql","oracle","oracle+cx_oracle","mssql+pyodbc","mssql+pymssql"]:
        return URL.create(
            DB_PROTOCOLE,
            username=DB_USERNAME,
            password=str(DB_PASSWORD),
            host=DB_HOST,
            database=DB_NAME,
        )