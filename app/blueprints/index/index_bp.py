from flask import Blueprint, redirect, url_for, request

from app import current_user, logout_user, app

from config import *


index_bp = Blueprint("index", __name__, template_folder="templates")

log = app.logger


@index_bp.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        if current_user.role == "Admin":
            return redirect(url_for("panel.dashboard.index"))
        elif current_user.role == "User":
            return redirect(url_for("browser.index"))
    else:
        return redirect("/login")
