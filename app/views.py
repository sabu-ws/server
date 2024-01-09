from app import app, CSRFError
from app.first_init import database_init

from flask import redirect, url_for, flash, render_template

from app.blueprints.login.login_bp import login_bp
from app.blueprints.browser.browser_bp import browser_bp
from app.blueprints.panel.panel_bp import panel_bp
from app.blueprints.index.index_bp import index_bp
from app.blueprints.api.api_bp import api_bp
from app.blueprints.user.user_bp import user_bp


app.register_blueprint(index_bp)
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(api_bp, url_prefix="/api/v2")
app.register_blueprint(browser_bp, url_prefix="/browser")
app.register_blueprint(panel_bp, url_prefix="/panel")
app.register_blueprint(user_bp, url_prefix="/user")


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Bad CSRF token", "error")
    print("bad csrf")
    return redirect(url_for("login.login"))


@app.errorhandler(404)
def error404(error):
    return render_template("error/404.html")


database_init()
