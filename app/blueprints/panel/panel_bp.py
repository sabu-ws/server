from flask import Blueprint, redirect, url_for

from app.blueprints.panel.alerts.alerts_bp import alerts_bp
from app.blueprints.panel.browser.browser_bp import browser_bp
from app.blueprints.panel.dashboard.dashboard_bp import dashboard_bp
from app.blueprints.panel.endpoint.endpoint_bp import endpoint_bp
from app.blueprints.panel.home.home_bp import home_bp
from app.blueprints.panel.logs.logs_bp import logs_bp
from app.blueprints.panel.server.server_bp import server_bp
from app.blueprints.panel.usb.usb_bp import usb_bp
from app.blueprints.panel.users.users_bp import users_bp
from app.blueprints.panel.settings.settings_bp import settings_bp

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

panel_bp.register_blueprint(home_bp, url_prefix="/")
panel_bp.register_blueprint(alerts_bp, url_prefix="/alerts")
panel_bp.register_blueprint(browser_bp, url_prefix="/browser")
panel_bp.register_blueprint(dashboard_bp, url_prefix="/dashboard")
panel_bp.register_blueprint(logs_bp, url_prefix="/logs")
panel_bp.register_blueprint(server_bp, url_prefix="/server")
panel_bp.register_blueprint(usb_bp, url_prefix="/usb")
panel_bp.register_blueprint(users_bp, url_prefix="/users")
panel_bp.register_blueprint(settings_bp, url_prefix="/settings")
panel_bp.register_blueprint(endpoint_bp, url_prefix="/endpoints")
