from flask import Blueprint, render_template

from config import *

server_bp = Blueprint(
	"server",
	__name__
	)

@server_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")