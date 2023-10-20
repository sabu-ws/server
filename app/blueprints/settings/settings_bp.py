from flask import Blueprint

from app import login_required

from config import *

settings_bp = Blueprint(
	"settings",
	__name__,
	template_folder="templates"
	)

@settings_bp.route("/",methods=["GET","POST"])
@login_required
def settings():
	return "comming soon"
	return render_template("profil-settings.html")