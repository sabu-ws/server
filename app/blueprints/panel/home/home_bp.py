from flask import Blueprint, redirect, url_for

from config import *

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return redirect(url_for("panel.dashboard.index"))
