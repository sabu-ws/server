import psutil

import socket

import time
import datetime
from app import logger as log


def NET_get_ip_server():
    interfaces = NET_list_interfaces()
    ip = ""
    for interface in interfaces:
        for snic in psutil.net_if_addrs()[interface]:
            if snic.family == socket.AF_INET:
                ip = snic.address
                break
        if ip != "":
            break
    return ip


def NET_list_interfaces():
    return [
        interface
        for interface in list(psutil.net_if_addrs().keys())
        if interface != "lo"
        if "avahi" not in interface
    ]


def NET_get_network_speed(interval=0.5):
    """
    Get the network speed on all interface on this server.
    Return total_bytes_receive, total_bytes_send
    """
    tot_bytes_rcv = psutil.net_io_counters().bytes_recv
    tot_bytes_snd = psutil.net_io_counters().bytes_sent
    time.sleep(interval)
    tot_bytes_rcv = psutil.net_io_counters().bytes_recv - tot_bytes_rcv
    tot_bytes_snd = psutil.net_io_counters().bytes_sent - tot_bytes_snd

    return tot_bytes_rcv, tot_bytes_snd


def SYS_get_hostname():
    hostname = socket.gethostname()
    return hostname


def SYS_get_uptime():
    boot_time_timestamp = psutil.boot_time()
    dt_boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)

    dt_now = datetime.datetime.now()
    dt_diff = dt_now - dt_boot_time

    total_seconds = dt_diff.total_seconds()

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if int(days) >= 0:
        uptime = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"
    else:
        uptime = f"{int(hours)} hours, {int(minutes)} minutes"
    return uptime
