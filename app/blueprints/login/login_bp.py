from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    abort,
    session,
    make_response,
)

from app import (
    app,
    login_user,
    logout_user,
    login_required,
    current_user,
    bcrypt,
    db,
    logger as log,
)

from app.forms import LoginForm
from app.models import Users, Job
from config import *

import datetime
import jwt
import pyotp
import uuid
import hashlib
import os

login_bp = Blueprint("login", __name__, template_folder="templates")


def check_user():
    if "next" in request.args:
        return redirect(request.args["next"])
    if current_user.role == "Admin":
        session["job"] = Job.query.filter_by(id=current_user.job_id).first().name
        return redirect(url_for("panel.dashboard.index", _method="GET"))
    elif current_user.role == "User":
        session["job"] = Job.query.filter_by(id=current_user.job_id).first().name
        return redirect(url_for("browser.index", _method="GET"))
    else:
        abort(404)


def check_token():
    if "sabu" in request.cookies:
        try:
            data_prev = jwt.decode(
                request.cookies["sabu"], options={"verify_signature": False}
            )
            user = Users.query.filter_by(username=data_prev["username"]).first()
            if user is not None:
                if user.cookie != None:
                    data = jwt.decode(
                        request.cookies["sabu"], user.cookie, algorithms=["HS256"]
                    )
                    login_user(user)
        except jwt.ExpiredSignatureError:
            pass
        finally:
            pass

def init_connection(user):
    session["job"] = Job.query.filter_by(id=user.job_id).first().name
    del session["totp"]
    set_time = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    random_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    jwt_token = jwt.encode({"username": user.username,"exp": set_time,"iss": "SABU",},random_key,algorithm="HS256",)
    user.cookie = random_key
    db.session.commit()
    resp = make_response(render_template("login.html", con="ok"))
    resp.set_cookie("sabu",jwt_token,expires=datetime.datetime.now()+ datetime.timedelta(hours=12),secure=True,httponly=True,)
    login_user(user)
    log.info(f"User {user.username} has logged in")
    user_root_data_path = "/sabu/data"
    user_data_path = os.path.join(user_root_data_path,"data",user.username)
    user_qurantine_path = os.path.join(user_root_data_path,"quarantine",user.username)
    log.info(user_data_path)
    if not os.path.exists(user_data_path):
        os.mkdir(user_data_path)
        log.info(f"Data user path create : {str(user_data_path)} ")
    if not os.path.exists(user_qurantine_path):
        os.mkdir(user_qurantine_path)
        log.info(f"Data user path create : {str(user_qurantine_path)} ")

    return resp

@login_bp.route("/", methods=["GET", "POST"])
def login():
    session["totp"] = False
    check_token()
    if current_user.is_authenticated is True:
        return check_user()
    if request.method == "POST":
        data = dict(request.form)
        form = LoginForm(data=data)
        if form.password.validate(form):
            user = Users.query.filter_by(username=form.username.data).first()
            if user is not None:
                if user.enable == 1:
                    if bcrypt.check_password_hash(user.password, form.password.data):
                        session["user"] = user.username
                        if user.OTPSecret is not None:
                            session["totp"] = True
                            return redirect(url_for("login.mfa"))
                        elif user.firstCon == 0:
                            return redirect(url_for("login.first_con"))
                        else:
                            return init_connection(user)
                    else:
                        return render_template("login.html", con="ko")
                else:
                    return render_template("login.html", con="ko")
            else:
                return render_template("login.html", con="ko")
        return render_template("login.html", con="ko")
    return render_template("login.html")


@login_bp.route("/mfa", methods=["GET", "POST"])
def mfa():
    if "totp" in session:
        if session["totp"] is True:
            if request.method == "POST":
                data = dict(request.form)
                user = Users.query.filter_by(username=session["user"]).first()
                totp = pyotp.TOTP(user.OTPSecret)
                if totp.verify(data["totp"]):
                    return init_connection(user)
                else:
                    log.info(f"User {user.username} enter bad totp")
                    return render_template("login_totp.html", con="ko")
        else:
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))
    return render_template("login_totp.html")


@login_bp.route("/first_connection", methods=["GET", "POST"])
def first_con():
    if "user" in session:
        if current_user.is_authenticated is True:
            return check_user()
        user = Users.query.filter_by(username=session["user"]).first()
        if request.method == "POST":
            data = request.form
            if "newPasswordInput" in data and "repeatPasswordInput" in data:
                if data["newPasswordInput"] == data["repeatPasswordInput"]:
                    dataf = {
                        "username": session["user"],
                        "password": data["newPasswordInput"],
                    }
                    form = LoginForm(data=dataf)
                    if form.validate():
                        user.firstCon = 1
                        user.set_password(data["newPasswordInput"])
                        db.session.commit()
                        return init_connection(user)
                    else:
                        return render_template(
                            "login_first_con.html",
                            con="ko",
                            error=form.errors["password"][0],
                        )
                else:
                    return render_template(
                        "login_first_con.html",
                        con="ko",
                        error="The password fields are not the same.",
                    )
            else:
                return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))
    return render_template("login_first_con.html")


@login_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    username = str(current_user.username)
    user = Users.query.filter_by(username=username).first()
    user.cookie = None
    db.session.commit()
    log.info(f"User {username} has logged out ")
    logout_user()
    resp = make_response(redirect(url_for("login.login")))
    if "sabu" in request.cookies:
        resp.delete_cookie("sabu")
    return resp
