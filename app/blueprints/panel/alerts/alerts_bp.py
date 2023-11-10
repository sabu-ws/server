from flask import Blueprint, render_template

from config import *

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/")
def index():
    return render_template("ap_coming_soon.html")
