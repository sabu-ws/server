from flask import Blueprint, render_template

from config import *

dashboard_bp = Blueprint(
	"dashboard",
	__name__
	)

@dashboard_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")