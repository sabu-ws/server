from config import *
from app.celery import scanner
from core.scripts.tmp.scan_yara import scan_yara

import time
import subprocess
import os


@scanner.task
def clamav(cuuid, id_scan):
    guuid = str(cuuid)
    scan_path = os.path.join(DATA_PATH, "scan", guuid)
    quarantine_path = os.path.join(DATA_PATH, "quarantine", guuid)
    log_path = f"/sabu/logs/server/scan/{str(id_scan)}"
    command = f"/usr/bin/bash /sabu/server/core/scripts/scan_clamav.sh -s {scan_path} -q {quarantine_path} -l {log_path}".split()
    resultat = (
        subprocess.Popen(command, stdout=subprocess.PIPE)
        .communicate()[0]
        .decode()
        .split("\n")[-1]
    )
    res_split = resultat.split(";")
    number = res_split[1]
    return number


@scanner.task
def yara(cuuid, id_scan):
    guuid = str(cuuid)
    scan_path = os.path.join(DATA_PATH, "scan", guuid)
    quarantine_path = os.path.join(DATA_PATH, "quarantine", guuid)
    log_path = f"/sabu/logs/server/scan/{str(id_scan)}"
    resultat = scan_yara(
        "/sabu/server/core/yararules/index.yar", scan_path, quarantine_path, log_path
    )
    res_split = resultat.split(";")
    number = res_split[1]
    return number
