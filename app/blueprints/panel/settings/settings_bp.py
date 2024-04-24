from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import socketio,emit,db
from app.models import Extensions, Setup

import os
import subprocess
import datetime

from app import logger as log

from config import *

settings_bp = Blueprint("settings", __name__)

@socketio.on("extension_show",namespace="/settings")
def show_extension():
    get_valid_ext = Extensions.query.filter_by(valid=True).all()
    valid_extension =  [ext.extension for ext in get_valid_ext]
    emit("extension_get",valid_extension)
    emit("log")

@socketio.on("extension_add",namespace="/settings")
def show_extension(data):
    if_ext_exist_valid = Extensions.query.filter_by(valid=False,extension=data).first()
    if if_ext_exist_valid:
        if_ext_exist_valid.valid=True
        db.session.commit()
        emit("extension_add_rcv","ok")
    else:
        if_ext_exist_nvalid = Extensions.query.filter_by(valid=True,extension=data).first()
        if if_ext_exist_nvalid:
            emit("extension_add_rcv","exist")
        else:
            emit("extension_add_rcv","nexist")
    return

@socketio.on("extension_del",namespace="/settings")
def show_extension(data):
    if_ext_exist_valid = Extensions.query.filter_by(valid=True,extension=data).first()
    if if_ext_exist_valid:
        if_ext_exist_valid.valid=False
        db.session.commit()


@settings_bp.route("/")
def index():
    db_ret = Setup.query.filter_by(action="ret").first().value
    db_appc = Setup.query.filter_by(action="appc").first().value
    db_appt = Setup.query.filter_by(action="appt").first().value

    return render_template("ap_settings.html",ret=db_ret,appc=db_appc,appt=db_appt)

@settings_bp.route("/maintenance",methods=["POST"])
def maintenance():
    data_retention = request.form["amountInput"]
    data_appc = request.form["selectRetCircle"]
    data_appt = request.form["appt"]
    if 1<=int(data_retention)<=90:
        db_ret = Setup.query.filter_by(action="ret").first()
        db_ret.value = data_retention
    else:
        flash("Error retention value","error")
    if data_appc in ["ED","EW","EM"]:
        db_appc = Setup.query.filter_by(action="appc").first()
        db_appc.value = data_appc
    else:
        flash("Error menu maintenance value","error")
    data_appt_hour = data_appt.split(":")[0]
    data_appt_minute = data_appt.split(":")[1]
    if 0<=int(data_appt_hour)<=24 or 0<=int(data_appt_hour)<=60:
        db_appt = Setup.query.filter_by(action="appt").first()
        db_appt.value = data_appt
        db.session.commit()
    else:
        flash("Error time maintenance value","error")
    return redirect(url_for("panel.settings.index"))