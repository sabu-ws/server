from flask import Blueprint, redirect, url_for

from app import login_required, current_user, logout_user

browser_bp = Blueprint(
	"browser",
	__name__,
	template_folder="templates"
	)

@browser_bp.before_request
@login_required
def before_request_browser_bp():
	if current_user.role != "User":
		logout_user()
		return redirect(url_for("login.login"))

@browser_bp.route("/")
def index():
	return "comming soon"