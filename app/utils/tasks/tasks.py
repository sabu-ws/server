from config import *

from app import app
from app import db
from app.models import Metrics, Devices, Setup
from app.utils.system import NET_get_network_speed
from app import logger as log

import subprocess
import os


def read_CPU():
    with app.app_context():
        script = os.path.join(SCRIPT_PATH, "get_cpu_space.sh")
        result = (
            subprocess.Popen(["bash", script], stdout=subprocess.PIPE)
            .communicate()[0]
            .decode()
            .replace("\n", "")
        )
        get_device = Devices.query.filter_by(token="server").first()
        add_metrics = Metrics(name="cpu", value=int(result), idDevice=get_device.id)
        db.session.add(add_metrics)
        db.session.commit()


def read_RAM():
    with app.app_context():
        script = os.path.join(SCRIPT_PATH, "get_ram_space.sh")
        result = (
            subprocess.Popen(["bash", script], stdout=subprocess.PIPE)
            .communicate()[0]
            .decode()
            .replace("\n", "")
            .split(" ")[0]
        )
        get_device = Devices.query.filter_by(token="server").first()
        add_metrics = Metrics(name="ram", value=int(result), idDevice=get_device.id)
        db.session.add(add_metrics)
        db.session.commit()


def read_NET():
    with app.app_context():
        bytes_rcv, bytes_snd = NET_get_network_speed()
        get_device = Devices.query.filter_by(token="server").first()
        add_metrics_netin = Metrics(
            name="netin", value=int(bytes_rcv), idDevice=get_device.id
        )
        add_metrics_netout = Metrics(
            name="netout", value=int(bytes_snd), idDevice=get_device.id
        )
        db.session.add(add_metrics_netin)
        db.session.add(add_metrics_netout)
        db.session.commit()


def retention_files():
    with app.app_context():
        query_retention = Setup.query.filter_by(action="ret").first()
        if query_retention is not None:
            get_retention_value = query_retention.value
            path_to_script_retention = os.path.join(
                SCRIPT_PATH, "delete_files_older.sh"
            )
            commande = f"sudo /usr/bin/bash {path_to_script_retention} -p {DATA_PATH} -d {str(get_retention_value)} -r true".split()
            exec_retention = subprocess.Popen(commande)


def maitenance_server():
    log.info("maintenance server")
