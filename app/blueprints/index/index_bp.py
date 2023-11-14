from flask import Blueprint, redirect, url_for

from app import current_user

from config import *


index_bp = Blueprint("index", __name__, template_folder="templates")


@index_bp.route("/", methods=["GET"])
def index():
	if current_user.is_authenticated:
		if current_user.role == "Admin":
			return redirect(url_for("panel.users.index"))
		elif current_user.role == "User":
			return redirect(url_for("panel.users.index"))
	else:
		return redirect("/login")