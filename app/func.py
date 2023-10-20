from app.blueprints.admin.admin_bp import admin_bp
from app.blueprints.browser.browser_bp import browser_bp
from app import current_user
from flask import redirect, url_for

from functools import wraps


@admin_bp.before_request
@login_required
def admin_before_request():
	if current_user.role != "Admin":
		logout_user()
		return redirect(url_for("login.login"))


@browser_bp.before_request
@login_required
def before_request_browser_bp():
	if current_user.role != "User":
		logout_user()
		return redirect(url_for("login.login"))