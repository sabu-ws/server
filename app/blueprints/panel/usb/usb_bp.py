from flask import Blueprint, render_template

from config import *

usb_bp = Blueprint(
	"usb",
	__name__
	)

@usb_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")