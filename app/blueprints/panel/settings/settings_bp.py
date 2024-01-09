from flask import Blueprint, render_template

from config import *

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/")
def index():
    return render_template("ap_settings.html")
