from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import logout_user
from app.utils import getHostname
from config import *

import OpenSSL
import re

server_bp = Blueprint(
	"server",
	__name__
	)


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
		if 5 < len(request.form["hostname"]) < 64:
			regex = r'^[a-zA-Z0-9-]{5,64}$'
			print(re.match(regex,request.form["hostname"]))
			if re.match(regex,request.form["hostname"]):
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