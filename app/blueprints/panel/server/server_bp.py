from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import logout_user, socketio
from app.utils import getHostname
from app.func import read_and_forward_pty_output
from config import *

import subprocess
import OpenSSL
import re
import os

server_bp = Blueprint(
	"server",
	__name__
	)

# ================= start socket io func

@socketio.on("startLogsServer",namespace="/logServer")
def startLogsServer():
	temp_send_file = open("/var/log/syslog").read()
	modify_syslog = os.stat("/var/log/syslog")[9] # modify time
	temp_modify_syslog =  ""
	while True:
		socketio.sleep(1)
		if temp_modify_syslog != modify_syslog:
			temp_modify_syslog = modify_syslog
			file_syslog = open("/var/log/syslog").read()
			socketio.emit("receiveLogs",file_syslog,namespace="/logServer")
		else:
			modify_syslog = os.stat("/var/log/syslog")[9]

@socketio.on("connect",namespace="/pty")
def new_connextion():
	logf = open("log.txt","a")
	logf.write(f"new connexion {request.sid}\n")
	(pty_pid, fd) = pty.fork()
	session["fd"] = fd
	session["pid"] = pty_pid
	if pty_pid == 0:
		# os.execl('/usr/bin/ssh','ssh','root@localhost')
		os.execl('/bin/bash','bash')
	else:
		status = psutil.Process(pty_pid).status()
		socketio.start_background_task(read_and_forward_pty_output, fd, pty_pid,rooms()[0])

@socketio.on("disconnect",namespace="/pty")
def disconnect_user():
	logf = open("log.txt","a")
	logf.write(f"session {request.sid} was end\n")
	pty_pid = psutil.Process(session["pid"])
	logf.write(f"status child process {pty_pid.status()}\n")
	if pty_pid.status() in ('running', 'sleeping'):
		pty_pid.terminate()

@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
	"""write to the child pty, which now is the ssh process from this machine to the 'domain' configured
	"""
	try:
		child_process = psutil.Process(session["pid"])
	except psutil.NoSuchProcess as err:
		disconnect()
		return
	if child_process.status() not in ('running', 'sleeping'):
		disconnect()
		return
	fd = session["fd"]
	if fd:
		os.write(fd, data["input"].encode())

@socketio.on("resize", namespace="/pty")
def resize(data):
	try:
		child_process = psutil.Process(session["pid"])
	except psutil.NoSuchProcess as err:
		disconnect()
		return
	if child_process.status() not in ('running', 'sleeping'):
		disconnect()
		return
	fd = session["fd"]
	if fd:
		winsize = struct.pack("HHHH", data["rows"], data["cols"], 0, 0)
		fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

# ================= end socket io func


# ================ start router server

@server_bp.route("/")
def index():
	print(getHostname())
	return render_template("ap_srv_dashboard.html")


@server_bp.route("/logs")
def logs():
	return render_template("ap_srv_logs.html")


@server_bp.route("/settings")
def settings():
	return render_template("ap_srv_settings.html",hostname=getHostname())

@server_bp.route("/settings/hostname", methods=["POST"])
def settings_hostname():
	if "hostname" in request.form:
		if 5 <= len(request.form["hostname"]) <= 64:
			regex = r'^[a-zA-Z0-9-]{5,64}$'
			if re.match(regex,request.form["hostname"]):
				hostname = str(request.form["hostname"])
				command = f"sudo bash /sabu/server/core/scripts/update_hostname.sh -n {hostname}".split()
				subprocess.Popen(command)
				flash("The hostname has been change","good")
				return redirect(url_for("panel.server.settings"))
			else:
				flash("You enter bad charactere for the hostname!","error")
				return redirect(url_for("panel.server.settings"))
		else:
			flash("Please enter hostname between 5 and 64 charactère","error")
			return redirect(url_for("panel.server.settings"))

	else:
		logout_user()
		return redirect(url_for("login.logn"))
	return ""

@server_bp.route("/settings/certificates", methods=["POST"])
def settings_certificates():
	if "fileCRT" in request.files and "fileKEY" in request.files:
		crt_file = request.files["fileCRT"]
		key_file = request.files["fileKEY"] 
		if crt_file.filename != "" and key_file.filename != "" :
			if  crt_file.mimetype != "application/x-x509-ca-cert" and crt_file.filename[-4:] != ".crt"  :
				flash("Please input correct type of certificate file !","error")
				return redirect(url_for("panel.server.settings"))
			if key_file.mimetype != "application/octet-stream"  and key_file.filename[-4:] != ".key" :
				flash("Please input correct type of key file !","error")
				return redirect(url_for("panel.server.settings"))
			passphrase_private_key = b""
			if "phassphraseKeyFile" in request.form:
				if request.form["phassphraseKeyFile"] != "":
					passphrase_private_key = request.form["phassphraseKeyFile"].encode()
			try:
				private_key_obj = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_file.read().decode(),passphrase=passphrase_private_key)
			except OpenSSL.crypto.Error:
				flash("Private Key file is not correct format !","error")
				return redirect(url_for("panel.server.settings"))
			try:
				cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, crt_file.read().decode())
			except OpenSSL.crypto.Error:
				flash("Certificate file is not correct format !","error")
				return redirect(url_for("panel.server.settings"))
			context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
			context.use_privatekey(private_key_obj)
			context.use_certificate(cert_obj)
			try:
				print(context.check_privatekey())
			except OpenSSL.SSL.Error:
				flash("The corresponding between certificate and key files is not coorect !","error")
				return redirect(url_for("panel.server.settings"))

			# ========================================== for tempory 

			# shutil.move("/sabu/nginx/certificates/sabu-gui.crt", "/sabu/nginx/certificates/sabu-gui.crt.old")				
			# shutil.move("/sabu/nginx/certificates/sabu-gui.key", "/sabu/nginx/certificates/sabu-gui.key.old")
			path = "/temp/"
			import tempfile
			tempfile.TemporaryFile().write(crt_file.read())
			tempfile.TemporaryFile().write(key_file.read())
			# crt_file.save(path+"e")
			# key_file.save(path+"m")
			# ==========================================

			flash("The certificates and private key file has been change","good")
			return redirect(url_for("panel.server.settings"))
		else:
			flash("Please select certificate and key files !","error")
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