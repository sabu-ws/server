from flask import Blueprint, render_template
from app.models import Devices
from config import *

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    devices=Devices.query.filter(Devices.token!="server").all()
    return render_template("ap_dashboard.html", list_devices=devices)
    
