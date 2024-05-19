from app import logger as log, db
from app.models import Devices, USBlog
from app.utils.system import NET_get_ip_server
from app.utils.system import SYS_get_hostname, SYS_get_uptime
from config import *

from flask import Blueprint, render_template
from sqlalchemy import text
import datetime

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    # get Endpoint device
    devices = Devices.query.filter(Devices.token != "server").all()
    number_endpoint_on = (
        Devices.query.filter(Devices.token != "server")
        .filter(Devices.state == 1)
        .count()
    )
    number_endpoint_tot = len(devices)

    # Server information
    server_ip = NET_get_ip_server()
    hostname = SYS_get_hostname()
    uptime = SYS_get_uptime()
    version = SABU_VERSION
    licence = SABU_LICENCE

    # Scan information
    with db.engine.connect() as con:
        #result of this var is : [datetime, nb virus detected, nb all virus in this day] 
        scan_per_day = con.execute(text(   
               "SELECT time_bucket('1 day', date_ht) AS bucket, SUM(virus) as nb_virus, COUNT(*) as nb_scan FROM usblog GROUP BY bucket ORDER BY bucket ASC LIMIT 7;"
           )).all()
    _7day_virus_scan = [[i[0].strftime("%D"),i[1],i[2]] for i in scan_per_day]
    sum_scan_7day = sum([i[2] for i in scan_per_day])
    sum_virus_7day = sum([i[1] for i in scan_per_day])

    # all_scan = USBlog.query

    return render_template(
        "ap_dashboard.html",
        number_endpoint_on=number_endpoint_on,
        number_endpoint_tot=number_endpoint_tot,
        all_scan_7day=sum_scan_7day,
        all_virus_7day=sum_virus_7day,
        _7day_virus_scan=_7day_virus_scan,
        list_devices=devices,
        hostname=hostname,
        uptime=uptime,
        server_ip=server_ip,
        version=version,
        licence=licence,
    )
