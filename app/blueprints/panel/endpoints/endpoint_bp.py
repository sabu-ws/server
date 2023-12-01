from config import *

from app import logout_user, db, socketio, app
from app.models import Devices

from flask import Blueprint, render_template, request, session, flash
import re
import jwt
import random
import datetime
import hashlib
import uuid

endpoint_bp = Blueprint("endpoints", __name__)

# Use for send info to page
@socketio.on("connect",namespace="/state_ep")
def new_con(data):
	return 0

@endpoint_bp.route("/")
def index():
	devices=Devices.query.filter(Devices.token!="server").all()
	return render_template("ap_ep_index.html",list_devices=devices)

@endpoint_bp.route("/add_endpoint",methods=["POST"])
def add_endpoint():
	if "endpointToken" in request.form and "endpointHostname" in request.form:
		hostname_regex = r"^[a-zA-Z0-9-]{5,64}$"
		if re.match(hostname_regex,request.form["endpointHostname"]):
			if request.form["endpointToken"] != "" and "temp_token" in session:
				if request.form["endpointToken"] == session["temp_token"]:
					api_token = session["temp_token_pass"]
					del session["temp_token"]
					del session["temp_token_pass"]
					add_device = Devices(hostname=request.form["endpointHostname"],token=api_token)
					db.session.add(add_device)
					db.session.commit()
					return "ok"
				else:
					logout_user()
					return "ok"
			else:
				return "Please generate a token"
		else:
			return "Please enter a correct hostname for the endpoint"
	else:
		logout_user()
		return "ok"


@endpoint_bp.route("/gen_ep_token")
def gen_ep_token():
	set_time = datetime.datetime.utcnow() + datetime.timedelta(days=365)
	random_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
	session["temp_token_pass"] = random_key
	jwt_token = jwt.encode({
			"exp": set_time,
			"iss": "SABU",
		},
		random_key,
		algorithm="HS256",
	)
	session["temp_token"] = jwt_token
	return jwt_token

@endpoint_bp.route("/delete_endpoint",methods=["POST"])
def delete_endpoint():
	if "uuid" in request.form:
		guuid=request.form["uuid"]
		if guuid != "":
			ep_qry = Devices.query.filter_by(uuid=uuid.UUID(guuid)).first()
			if ep_qry != None:
				db.session.delete(ep_qry)
				db.session.commit()
				name_ep = ep_qry.hostname
				flash(f"Endpoint {name_ep} has been delete","good")
				return "ok"
		else:
			logout_user()
			return "ok"
	else:
		logout_user()
		return "ok"
	return ""


@endpoint_bp.route("/dashboard")
def dashboard():
	return render_template("ap_ep_dashboard.html")


# @endpoint_bp.route("/logs")
# def logs():
# 	return render_template("ap_ep_logs.html")


@endpoint_bp.route("/settings")
def settings():
	return render_template("ap_ep_settings.html")
