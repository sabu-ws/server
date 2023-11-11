from flask import Blueprint, render_template

from config import *

endpoint_bp = Blueprint("endpoint", __name__)


@endpoint_bp.route("/")
def index():
    return render_template("ap_ep_index.html")


@endpoint_bp.route("/dashboard")
def dashboard():
	return render_template("ap_ep_dashboard.html")


# @endpoint_bp.route("/logs")
# def logs():
# 	return render_template("ap_ep_logs.html")


@endpoint_bp.route("/settings")
def settings():
	return render_template("ap_ep_settings.html")