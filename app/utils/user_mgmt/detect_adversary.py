from app import logout_user, app
from flask import make_response


def force_logout_user():
    app.logger.warning("Adversary detected")
    logout_user()
    resp = make_response("ok")
    resp.delete_cookie("sabu")
    resp.delete_cookie("session")
    return resp
