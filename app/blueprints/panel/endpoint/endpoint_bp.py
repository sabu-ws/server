from flask import Blueprint, render_template

from config import *

endpoint_bp = Blueprint(
	"endpoint",
	__name__
	)

@endpoint_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")