from flask import Blueprint, render_template

from config import *

home_bp = Blueprint(
	"home",
	__name__
	)

@home_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")