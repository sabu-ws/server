from flask import Blueprint, render_template

from config import *

server_bp = Blueprint(
	"server",
	__name__
	)

@server_bp.route("/")
def index():
	return render_template("ap_srv_dashboard.html")

@server_bp.route("/logs")
def logs():
	return render_template("ap_coming_soon.html")

@server_bp.route("/settings")
def settings():
	return render_template("ap_srv_settings.html")