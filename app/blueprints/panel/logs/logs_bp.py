from flask import Blueprint, render_template

from config import *

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/")
def index():
    return render_template("ap_logs.html")
