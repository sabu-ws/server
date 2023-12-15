from flask import Blueprint, render_template
from app.models import Devices
from app.utils.system import NET_get_ip_server
from app.utils.system import SYS_get_hostname, SYS_get_uptime
from config import *

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    devices = Devices.query.filter(Devices.token != "server").all()
    server_ip = NET_get_ip_server()
    hostname = SYS_get_hostname()
    uptime = SYS_get_uptime()
    version = SABU_VERSION
    licence = SABU_LICENCE
    return render_template(
        "ap_dashboard.html",
        list_devices=devices,
        hostname=hostname,
        uptime=uptime,
        server_ip=server_ip,
        version=version,
        licence=licence,
    )
