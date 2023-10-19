from flask import redirect, url_for, request
from app.utils import logging
from app.blueprints.admin.admin_bp import admin_bp
from app.blueprints.browser.browser_bp import browser_bp
from app import current_user
from Flask import redirect, url_for

from functools import wraps

# @app.before_request
# def setup_state():
#     if Setup.query.filter(Setup.action=="global", Setup.state==True).first() == None :
#         if request.path != "/setup":
#             return redirect(url_for("index.setup"))
#     else:
#         if request.path == "/setup":
#             logging("misc","something try to go setup page")
#             return redirect(url_for("index.index"))

@admin_bp.before_request
def before_request_admin_bp():
	return current_user.role
	if current_user.role != "admin":
		return "redirect to browser"
		# return redirect(url_for("browser.path"))

@browser_bp.before_request
def before_request_browser_bp():
	return current_user.role
	if current_user.role != "user":
		return "redirect to admin dashboard"
		# return redirect(url_for("admin.dashboard"))