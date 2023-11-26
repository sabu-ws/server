import psutil

import socket 
import subprocess
import time

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
    return [interface for interface in list(psutil.net_if_addrs().keys()) if interface != "lo" if "avahi" not in interface]

def NET_get_network_speed(interval=0.5):
    """
    Get the network speed on all interface on this server.
    Return total_bytes_receive, total_bytes_send
    """
    tot_bytes_rcv =  psutil.net_io_counters().bytes_recv
    tot_bytes_snd =  psutil.net_io_counters().bytes_sent
    time.sleep(interval)
    tot_bytes_rcv = psutil.net_io_counters().bytes_recv - tot_bytes_rcv
    tot_bytes_snd =  psutil.net_io_counters().bytes_sent - tot_bytes_snd

    return tot_bytes_rcv,tot_bytes_snd

def SYS_get_hostname():
    return (
        subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        .communicate()[0]
        .decode()
        .replace("\n", "")
    )
