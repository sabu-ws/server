from flask import Blueprint, render_template
from app import socketio, logger as log
from config import *

logs_bp = Blueprint("logs", __name__)

@socketio.on("startLogsSabu", namespace="/logServer")
def startLogsServer():
    temp_send_file = open("/sabu/logs/server/sabu.log").read()
    modify_syslog = os.stat("/sabu/logs/server/sabu.log")[9]  # modify time
    temp_modify_syslog = ""
    while True:
        socketio.sleep(1)
        if temp_modify_syslog != modify_syslog:
            temp_modify_syslog = modify_syslog
            file_syslog = open("/sabu/logs/server/sabu.log").read()
            restrict_len = file_syslog[len(file_syslog)-100000:]
            socketio.emit("receiveLogsSabu", restrict_len, namespace="/logServer")
        else:
            modify_syslog = os.stat("/sabu/logs/server/sabu.log")[9]

@logs_bp.route("/")
def index():
    return render_template("ap_logs.html")
