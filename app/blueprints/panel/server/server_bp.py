from config import *

from app import socketio, db, logger as log
from app.models import Devices, Metrics
from app.forms import ModifyIpForm
from app.utils.system import (
	SYS_get_hostname,
	NET_list_interfaces,
	NET_get_network_speed,
)

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import desc

import datetime
import subprocess
import OpenSSL
import shutil
import os
import re

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


from sqlalchemy import func
@socketio.on("start_chart_cpu_rcv", namespace="/chart_CPU")
def connect_chart_cpu():
	table_cpu = []
	get_server_device = Devices.query.filter_by(token="server").first()
	delta_hours = datetime.datetime.now() - datetime.timedelta(hours=24)
	get_cpu_metrics = (
		Metrics.query.filter(Metrics.idDevice==int(get_server_device.id), Metrics.name=="cpu",Metrics.timestamp_ht >= delta_hours)
		.all()
	)
	
	for metric in get_cpu_metrics:
		format_datetime = metric.timestamp_ht.strftime("%Y-%m-%d %H:%M:%S")
		chart_metric = {"x": format_datetime, "y": metric.value}
		table_cpu.append(chart_metric)
	socketio.emit("chart_cpu_rcv", table_cpu, namespace="/chart_CPU")


@socketio.on("start_chart_ram_rcv", namespace="/chart_RAM")
def connect_chart_cpu():
	table_ram = []
	get_server_device = Devices.query.filter_by(token="server").first()
	delta_hours = datetime.datetime.now() - datetime.timedelta(hours=24)
	get_ram_metrics = (
		Metrics.query.filter(Metrics.idDevice==int(get_server_device.id), Metrics.name=="ram",Metrics.timestamp_ht >= delta_hours)
		.all()
	)
	for metric in get_ram_metrics:
		format_datetime = metric.timestamp_ht.strftime("%Y-%m-%d %H:%M:%S")
		chart_metric = {"x": format_datetime, "y": int(metric.value) / 1024 / 1024}
		table_ram.append(chart_metric)
	socketio.emit("chart_ram_rcv", table_ram, namespace="/chart_RAM")


@socketio.on("start_chart_disk_rcv", namespace="/chart_DISK")
def connect_chart_cpu():
	script = os.path.join(SCRIPT_PATH, "get_disk_space.sh")
	get_total_disk = (
		subprocess.Popen(["bash", script], stdout=subprocess.PIPE)
		.communicate()[0]
		.decode()
		.replace("\n", "")
		.split(" ")
	)
	socketio.emit("chart_disk_rcv", get_total_disk, namespace="/chart_DISK")


@socketio.on("start_chart_net_rcv", namespace="/chart_NET")
def connect_chart_net():
	table_netin = []
	table_netou = []
	get_server_device = Devices.query.filter_by(token="server").first()
	delta_hours = datetime.datetime.now() - datetime.timedelta(hours=24)
	get_netin_metrics = (
		Metrics.query.filter(Metrics.idDevice==int(get_server_device.id), Metrics.name=="netin",Metrics.timestamp_ht >= delta_hours)
		.all()
	)
	get_netout_metrics = (
		Metrics.query.filter(Metrics.idDevice==int(get_server_device.id), Metrics.name=="netout",Metrics.timestamp_ht >= delta_hours)
		.all()
	)
	for metric_netin, metric_netout in zip(get_netin_metrics,get_netout_metrics):
		format_datetime = metric_netin.timestamp_ht.strftime("%Y-%m-%d %H:%M:%S")
		chart_netin = {"x": format_datetime, "y": metric_netin.value}
		chart_netout = {"x": format_datetime, "y": metric_netout.value}
		table_netin.append(chart_netin)
		table_netou.append(chart_netout)
	table_netall = [table_netin,table_netou]
	socketio.emit("chart_net_rcv", table_netall, namespace="/chart_NET")


# ================= end socket io func


# ================ start router server


@server_bp.route("/")
def index():
	script = os.path.join(SCRIPT_PATH, "get_ram_space.sh")
	get_total_ram = (
		subprocess.Popen(["bash", script], stdout=subprocess.PIPE)
		.communicate()[0]
		.decode()
		.replace("\n", "")
		.split(" ")[1]
	)
	formating = int(get_total_ram) / 1024 / 1024

	return render_template(
		"ap_srv_dashboard.html", total_ram=float(f"{formating:3.1f}")
	)


@server_bp.route("/logs")
def logs():
	return render_template("ap_srv_logs.html")


@server_bp.route("/settings")
def settings():
	get_device = Devices.query.filter_by(token="server").first()
	return render_template(
		"ap_srv_settings.html",
		hostname=SYS_get_hostname(),
		device=get_device,
		interfaces=NET_list_interfaces(),
	)


@server_bp.route("/settings/hostname", methods=["POST"])
def settings_hostname():
	if (
		"hostname" in request.form or "description" in request.form
	) and "uuid" in request.form:
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
						flash("The hostname has been change", "good")
						log.info(f"The hostname has been change by {str(hostname)}")
						return redirect(url_for("panel.server.settings"))
					else:
						flash("You enter bad charactere for the hostname!", "error")
						return redirect(url_for("panel.server.settings"))
				else:
					flash("Please enter hostname between 5 and 64 charactère", "error")
					return redirect(url_for("panel.server.settings"))
		else:
			log.warning("Adversary detected")
			return redirect(url_for("login.logout"))
	else:
		log.warning("Adversary detected")
		return redirect(url_for("login.logout"))
	return ""


@server_bp.route("/settings/description", methods=["POST"])
def settings_description():
	if "description" in request.form and "uuid" in request.form:
		get_device = Devices.query.filter_by(uuid=request.form["uuid"]).first()
		if get_device != None:
			if request.form["description"] != "":
				if len(request.form["description"]) <= 1024:
					get_device.description = request.form["description"]
					db.session.commit()
					flash("The description has been change", "good")
					return redirect(url_for("panel.server.settings"))
				else:
					flash(
						"The description must have maximum 1024 charactere !", "error"
					)
					return redirect(url_for("panel.server.settings"))
		else:
			log.warning("Adversary detected")
			return redirect(url_for("login.logout"))
	else:
		log.warning("Adversary detected")
		return redirect(url_for("login.logout"))
	return ""


@server_bp.route("/settings/networks", methods=["POST"])
def settings_networks():
	if (
		"interface" in request.form
		and "ip" in request.form
		and "netmask" in request.form
		and "gateway" in request.form
		and "dns1" in request.form
		and "dns2" in request.form
	):
		if request.form["interface"] in NET_list_interfaces():
			form = ModifyIpForm(data=request.form)
			if ModifyIpForm.validate(form):
				dns2 = "9.9.9.9"
				if request.form["dns2"] != "":
					dns2 = request.form["dns2"]
				command = (
					"sudo /usr/bin/bash "
					+ os.path.join(SCRIPT_PATH, "update_ip_address.sh")
					+ f" -i {request.form['interface']} -a {request.form['ip']} -n {request.form['netmask']} -g {request.form['gateway']} -1 {request.form['dns1']} -2 {dns2}"
				)
				execute = (
					subprocess.Popen(command.split(), stdout=subprocess.PIPE)
					.communicate()[0]
					.decode()
				)
				flash("Sussesfull change network configuration", "good")
				return redirect(url_for("panel.server.settings"))
			else:
				keys = list(dict(form.errors.items()))
				flash(str(dict(form.errors.items())[keys[0]][0]), "error")
				return redirect(url_for("panel.server.settings"))
		else:
			log.warning("Adversary detected")
			return redirect(url_for("login.logout"))
	else:
		log.warning("Adversary detected")
		return redirect(url_for("login.logout"))
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
			log.info("The certificates and private key file has been change")
			return redirect(url_for("panel.server.settings"))
		else:
			flash("Please select certificate and key files !", "error")
			return redirect(url_for("panel.server.settings"))
	else:
		log.warning("Adversary detected")
		return redirect(url_for("login.logout"))
	return ""


@server_bp.route("/reboot")
def reboot():
	subprocess.Popen("sudo /usr/sbin/reboot -h now".split())
	flash("The server will be reboot","info")
	return "ok"


@server_bp.route("/shutdown")
def shutdown():
	subprocess.Popen("sudo /usr/sbin/shutdown -h now".split())
	flash("The server will be shutdown","info")
	return "ok"


@server_bp.route("/ssh")
def ssh():
	# https://github.com/Fisherworks/flask-remote-terminal/blob/master/app.py
	# https://docs.python.org/3/library/pty.html
	return render_template("ap_srv_ssh.html")

@server_bp.route("/test")
def test():
	return ""

# ================ end router server