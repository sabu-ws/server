from flask import Blueprint, redirect, url_for

from app.blueprints.panel.users.users_bp import users_bp
from app import login_required, current_user, logout_user

from config import *

panel_bp = Blueprint(
	"panel",
	__name__,
	template_folder="templates"
	)


@panel_bp.before_request
@login_required
def panel_before_request():
	if current_user.role != "Admin":
		logout_user()
		return redirect(url_for("login.login"))

panel_bp.register_blueprint(users_bp,url_prefix="/users")