from flask import Blueprint, redirect, url_for, request

from app import current_user, logout_user, app

from config import *


index_bp = Blueprint("index", __name__, template_folder="templates")

log = app.logger


@app.before_request
def before_index():
    if current_user.is_authenticated:
        if "sabu" not in request.cookies:
            username = str(current_user.username)
            user = Users.query.filter_by(username=username).first()
            user.cookie = None
            db.session.commit()
            logout_user()
            log.info(f"User {username} has logged out ")
            return redirect(url_for("login.login"))


@index_bp.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        if current_user.role == "Admin":
            return redirect(url_for("panel.dashboard.index"))
        elif current_user.role == "User":
            return redirect(url_for("browser.index"))
    else:
        return redirect("/login")
