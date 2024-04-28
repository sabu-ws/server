from app import logger as log, current_user, scanner, db
from app.models import Users,USBlog

from celery import group
from app.utils.scan import scan
import os
import uuid

def start_scan():
    cuuid = current_user.uuid
    uuid_taks_id = str(uuid.uuid4())
    scan_log_path = f"/sabu/logs/server/scan/{str(uuid_taks_id)}/" 
    os.makedirs(scan_log_path)
    group_tasks = group([
		scan.clamav.s(cuuid,uuid_taks_id),
    ])
    res = group_tasks.apply_async(task_id=uuid_taks_id)
    res.save()
    return uuid_taks_id

def end_scan(uuid_scan):
    resultat_task = scanner.GroupResult.restore(uuid_scan)
    element_res_task = resultat_task.get()
    default_virus = 0
    for number_virus in element_res_task:
        default_virus+=int(number_virus)
    cid = current_user.id
    user = Users.query.filter_by(id=cid).first()
    usblog = USBlog.query.filter_by(scan_id=uuid_scan).first()
    if usblog == None:
        contruct_usblog = USBlog(virus=default_virus,scan_id=uuid_scan,user_id=user.id)
        db.session.add(contruct_usblog)
        db.session.commit()
    return True