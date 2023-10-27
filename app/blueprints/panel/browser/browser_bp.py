from flask import Blueprint, render_template

from config import *

browser_bp = Blueprint(
	"browser",
	__name__
	)

@browser_bp.route("/")
def index():
	return render_template("ap_coming_soon.html")