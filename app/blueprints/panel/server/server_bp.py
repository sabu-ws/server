from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, rooms, disconnect

from app import logout_user, socketio, db
from app.utils import getHostname, list_interfaces
from app.models import Devices
from config import *

import subprocess
import OpenSSL
import re
import os
import shutil

server_bp = Blueprint("server", __name__)

# ================= start socket io func


@socketio.on("startLogsServer", namespace="/logServer")
def startLogsServer():
	temp_send_file = open("/var/log/syslog").read()
	modify_syslog = os.stat("/var/log/syslog")[9]  # modify time
	temp_modify_syslog = ""
	while True:
		socketio.sleep(1)
		if temp_modify_syslog != modify_syslog:
			temp_modify_syslog = modify_syslog
			file_syslog = open("/var/log/syslog").read()
			socketio.emit("receiveLogs", file_syslog, namespace="/logServer")
		else:
			modify_syslog = os.stat("/var/log/syslog")[9]


# ================= end socket io func


# ================ start router server


@server_bp.route("/")
def index():
	return render_template("ap_srv_dashboard.html")


@server_bp.route("/logs")
def logs():
	return render_template("ap_srv_logs.html")


@server_bp.route("/settings")
def settings():
	get_device = Devices.query.filter_by(token="server").first()
	return render_template("ap_srv_settings.html", hostname=getHostname(),device=get_device, interfaces=list_interfaces())


@server_bp.route("/settings/hostname", methods=["POST"])
def settings_hostname():
	if ("hostname" in request.form or "description" in request.form) and "uuid" in request.form:
		get_device = Devices.query.filter_by(uuid=request.form["uuid"]).first()
		if get_device != None:
			if request.form["hostname"] != "":
				if 5 <= len(request.form["hostname"]) <= 64:
					regex = r"^[a-zA-Z0-9-]{5,64}$"
					if re.match(regex, request.form["hostname"]):
						hostname = str(request.form["hostname"])
						command = f"sudo bash /sabu/server/core/scripts/update_hostname.sh -n {hostname}".split()
						subprocess.Popen(command)
						get_device.hostname = hostname
						db.session.commit()
						flash("The hostname has been change","good")
						return redirect(url_for("panel.server.settings"))
					else:
						flash("You enter bad charactere for the hostname!", "error")
						return redirect(url_for("panel.server.settings"))
				else:
					flash("Please enter hostname between 5 and 64 charactère", "error")
					return redirect(url_for("panel.server.settings"))
			
		else:
			logout_user()
			return redirect(url_for("login.logn"))
	else:
		logout_user()
		return redirect(url_for("login.logn"))
	return ""

@server_bp.route("/settings/description",methods=["POST"])
def settings_description():
	if "description" in request.form and "uuid" in request.form:
		get_device = Devices.query.filter_by(uuid=request.form["uuid"]).first()
		if get_device != None:
			if request.form["description"] != "":
				if len(request.form["description"])<=1024:
					get_device.description = request.form["description"]
					db.session.commit()
					flash("The description has been change","good")
					return redirect(url_for("panel.server.settings"))
				else:
					flash("The description must have maximum 1024 charactere !","error")
					return redirect(url_for("panel.server.settings"))
		else:
			logout_user()
			return redirect(url_for("login.logn"))
	else:
		logout_user()
		return redirect(url_for("login.logn"))
	return ""


@server_bp.route("/settings/certificates", methods=["POST"])
def settings_certificates():
	if "fileCRT" in request.files and "fileKEY" in request.files:
		crt_file = request.files["fileCRT"]
		key_file = request.files["fileKEY"]
		if crt_file.filename != "" and key_file.filename != "":
			if (
				crt_file.mimetype != "application/x-x509-ca-cert"
				and crt_file.filename[-4:] != ".crt"
			):
				flash("Please input correct type of certificate file !", "error")
				return redirect(url_for("panel.server.settings"))
			if (
				key_file.mimetype != "application/octet-stream"
				and key_file.filename[-4:] != ".key"
			):
				flash("Please input correct type of key file !", "error")
				return redirect(url_for("panel.server.settings"))
			passphrase_private_key = b""
			if "phassphraseKeyFile" in request.form:
				if request.form["phassphraseKeyFile"] != "":
					passphrase_private_key = request.form["phassphraseKeyFile"].encode()
			try:
				private_key_obj = OpenSSL.crypto.load_privatekey(
					OpenSSL.crypto.FILETYPE_PEM,
					key_file.read().decode(),
					passphrase=b"",
				)
			except OpenSSL.crypto.Error:
				flash("Private Key file is not correct format !", "error")
				return redirect(url_for("panel.server.settings"))
			try:
				cert_obj = OpenSSL.crypto.load_certificate(
					OpenSSL.crypto.FILETYPE_PEM, crt_file.read().decode()
				)
			except OpenSSL.crypto.Error:
				flash("Certificate file is not correct format !", "error")
				return redirect(url_for("panel.server.settings"))
			context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
			context.use_privatekey(private_key_obj)
			context.use_certificate(cert_obj)
			try:
				print(context.check_privatekey())
			except OpenSSL.SSL.Error:
				flash(
					"The corresponding between certificate and key files is not coorect !",
					"error",
				)
				return redirect(url_for("panel.server.settings"))
			private_key_dump = OpenSSL.crypto.dump_privatekey(
				OpenSSL.crypto.FILETYPE_PEM, private_key_obj
			)
			cert_dump = OpenSSL.crypto.dump_certificate(
				OpenSSL.crypto.FILETYPE_PEM, cert_obj
			)
			shutil.move("/sabu/ssl/sabu.crt", "/sabu/ssl/sabu.crt.old")
			shutil.move("/sabu/ssl/private/sabu.key", "/sabu/ssl/private/sabu.key.old")
			open("/sabu/ssl/sabu.crt", "wb").write(cert_dump)
			open("/sabu/ssl/private/sabu.key", "wb").write(private_key_dump)
			subprocess.Popen("sudo /usr/bin/systemctl restart nginx.service".split())
			subprocess.Popen("sudo /usr/bin/systemctl restart sabu.service".split())
			flash("The certificates and private key file has been change", "good")
			return redirect(url_for("panel.server.settings"))
		else:
			flash("Please select certificate and key files !", "error")
			return redirect(url_for("panel.server.settings"))
	else:
		logout_user()
		return ""
	return ""


@server_bp.route("/ssh")
def ssh():
	# https://github.com/Fisherworks/flask-remote-terminal/blob/master/app.py
	# https://docs.python.org/3/library/pty.html
	return render_template("ap_srv_ssh.html")


# ================ end router server
