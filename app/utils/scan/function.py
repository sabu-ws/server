from config import *
from app import logger as log, current_user, db
from app.utils.scan import scan
from app.models import Users, USBlog
from app.celery import scanner

from flask import session
from celery import group
import os
import shutil
import uuid


def start_scan():
    cuuid = current_user.uuid
    uuid_taks_id = str(uuid.uuid4())
    scan_log_path = f"/sabu/logs/server/scan/{str(uuid_taks_id)}/"
    os.makedirs(scan_log_path)
    group_tasks = group(
        [
            scan.clamav.s(cuuid, uuid_taks_id),
            scan.yara.s(cuuid, uuid_taks_id),
        ]
    )
    res = group_tasks.apply_async(task_id=uuid_taks_id)
    res.save()
    return str(uuid_taks_id)


def end_scan(uuid_scan):
    cuuid = current_user.uuid
    data_path = os.path.join(DATA_PATH, "data", str(cuuid))
    scan_path = os.path.join(DATA_PATH, "scan", str(cuuid))
    resultat_task = scanner.GroupResult.restore(uuid_scan)
    element_res_task = resultat_task.get()
    default_virus = 0
    for number_virus in element_res_task:
        default_virus += int(number_virus)
    cid = current_user.id
    user = Users.query.filter_by(id=cid).first()
    usblog = USBlog.query.filter_by(scan_id=uuid_scan).first()
    if usblog == None:
        contruct_usblog = USBlog(
            virus=default_virus, scan_id=uuid_scan, user_id=user.id
        )
        db.session.add(contruct_usblog)
        db.session.commit()
    for item in os.listdir(scan_path):
        grouping = os.path.join(scan_path, item)
        try:
            shutil.move(grouping, data_path)
        except:
            pass
    return True


def parse_result():
    last_scan_id = session.get("scan_id")
    cid = current_user.id
    user = Users.query.filter_by(id=cid).first()
    last_log_query = (
        USBlog.query.filter_by(user_id=cid).order_by(USBlog.date_ht.desc()).first()
    )
    if last_scan_id != None:
        if last_log_query != None:
            if last_log_query.virus == 0:
                if "scan_resultat" in session:
                    session["scan_resultat"].append("No virus found.")
            if last_log_query.virus > 0:
                if "scan_resultat" in session:
                    session["scan_resultat"].append(
                        f"Found {str(last_log_query.virus)} virus !"
                    )
                scan_log_path = f"/sabu/logs/server/scan/{str(last_scan_id)}/"
                for item in os.listdir(scan_log_path):
                    if "clamav" in item:
                        clamav_log_path = os.path.join(scan_log_path, item)
                        clamav_res = parse_clamav(clamav_log_path)
                    if "yara" in item:
                        yara_log_path = os.path.join(scan_log_path, item)
                        yara_res = parse_yara(yara_log_path)


def parse_clamav(log_file):
    file = open(log_file, "r")
    for line in file.readlines():
        if "FOUND" in line:
            seperate_file_malware = line.split(":")
            filename = seperate_file_malware[0].split("/")[-1]
            typed = seperate_file_malware[1].split()[0].strip()
            if "scan_resultat" in session:
                session["scan_resultat"].append(
                    f"The file '{filename}' is detected as malware : {typed} "
                )


def parse_yara(log_file):
    file = open(log_file, "r")
    for line in file.readlines():
        seperate_file_malware = line.split(" ", 1)
        filename = seperate_file_malware[1].strip().split("/")[-1]
        typed = seperate_file_malware[0]
        if "scan_resultat" in session:
            session["scan_resultat"].append(
                f"The file '{filename}' is detected as malware : {typed} "
            )
