from app.blueprints.admin.admin_bp import admin_bp
from app.blueprints.browser.browser_bp import browser_bp
from app import current_user
from flask import redirect, url_for

from functools import wraps


