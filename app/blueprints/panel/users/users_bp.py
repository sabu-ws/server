from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    jsonify,
    send_file,
    url_for,
)
import uuid
import re
from functools import wraps

from app import current_user, db, logger as log

from app.forms import AddUserForm
from app.models import Users, Job
from app.utils.user_mgmt import force_logout_user

from config import *


users_bp = Blueprint("users", __name__)


def check_is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "uuid" in request.form:
            if request.form["uuid"] != "":
                user = Users.query.filter_by(uuid=request.form["uuid"]).first()
                if user.username != "admin":
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for("login.logout"))
            else:
                return redirect(url_for("login.logout"))
        else:
            return redirect(url_for("login.logout"))

    return decorated_function


@users_bp.before_request
def users_bp_before_request():
    if current_user.is_authenticated is False:
        return redirect(url_for("login.login"))


@users_bp.route("/")
def index():
    get_user_list = Users.query.join(Job).all()
    get_job_name = Job.query.filter(Job.name != "Administrator").all()
    return render_template(
        "ap_users.html", userList=get_user_list, job_list=get_job_name
    )


@users_bp.route("/add_user", methods=["POST"])
def add_user():
    data = request.form
    if data["password"] == data["AddRepeatPassword"]:
        if (
            data["name"]
            and data["firstname"]
            and data["username"]
            and data["password"]
            and data["role"]
            and data["email"]
            and data["job"]
        ):
            form = AddUserForm(data=data)
            if data["job"] != "Choose a job":
                queryJob = Job.query.filter_by(name=data["job"]).first()
                if queryJob is not None and queryJob != "Administrator":
                    if AddUserForm.validate(form):
                        if (
                            Users.query.filter_by(username=data["username"]).first()
                            is None
                        ):
                            guuid = str(uuid.uuid4())
                            useradd = Users(
                                uuid=guuid,
                                username=data["username"],
                                name=data["name"],
                                firstname=data["firstname"],
                                role=data["role"],
                                email=data["email"],
                                job_id=queryJob.id,
                                enable=1,
                            )
                            useradd.set_password(data["password"])
                            db.session.add(useradd)
                            db.session.commit()
                            flash(f"New user added {data['username']}", "good")
                            log.info(
                                f"New user added {str(data['username'])} by {str(current_user.username)}"
                            )
                            return "ok"
                        else:
                            return "This username already exists"
                    else:
                        keys = list(dict(form.errors.items()))
                        return jsonify(dict(form.errors.items())[keys[0]][0])
                else:
                    return force_logout_user()
            else:
                return "Please select a job"
        else:
            return "Please fields all input"
    else:
        return "Password fields are not the same "


@users_bp.route("/mod_user", methods=["POST"])
@check_is_admin
def mod_user():
    data = request.form
    form = AddUserForm(data=data)
    if "uuid" in request.form:
        guuid = request.form["uuid"]
        queryUser = Users.query.filter_by(uuid=guuid).first()
        if queryUser is not None:
            if (
                form.firstname.validate(form)
                and form.name.validate(form)
                and form.username.validate(form)
                and form.role.validate(form)
                and form.email.validate(form)
            ):
                job = data["job"]
                if job not in ["Choose a job", "Administrator"]:
                    queryJob = Job.query.filter_by(name=job).first()
                    if queryJob is not None:
                        if (
                            request.form["password"] != ""
                            and request.form["EditRepeatPassword"] != ""
                        ):
                            if (
                                request.form["password"]
                                == request.form["EditRepeatPassword"]
                            ):
                                if form.password.validate(form):
                                    queryUser.set_password(data["password"])
                                else:
                                    keys = list(dict(form.errors.items()))
                                    return dict(form.errors.items())[keys[0]][0]
                            else:
                                return "Password fields are not the same"
                    else:
                        return force_logout_user()
                else:
                    return "Please select a job"
                queryUser.username = data["username"]
                queryUser.name = data["name"]
                queryUser.firstname = data["firstname"]
                queryUser.email = data["email"]
                queryUser.job_id = queryJob.id
                db.session.flush()
                db.session.commit()
                flash(
                    f"The informations of {queryUser.username} has been change", "good"
                )
                log.info(
                    f"The informations of user {str(queryUser.username)} has been change by {str(current_user.username)}"
                )
                return "ok"
            else:
                keys = list(dict(form.errors.items()))
                return jsonify(dict(form.errors.items())[keys[0]][0])
        else:
            return force_logout_user()
    else:
        return force_logout_user()
    return


@users_bp.route("/mod_user/query", methods=["POST"])
def mod_user_query():
    if "uuid" in request.form:
        guuid = request.form["uuid"]
        user = Users.query.filter_by(uuid=guuid).first()
        if user is not None:
            user.job_id = Job.query.filter_by(id=user.job_id).first().name
            return jsonify(
                {
                    "uuid": user.uuid,
                    "name": user.name,
                    "firstname": user.firstname,
                    "username": user.username,
                    "email": user.email,
                    "job": user.job_id,
                    "totp": True if user.OTPSecret else False,
                    "role": user.role,
                }
            )
        else:
            return force_logout_user()
    else:
        return force_logout_user()


@users_bp.route("/mod_user/disable_otp", methods=["POST"])
@check_is_admin
def mod_user_disable_otp():
    if "uuid" in request.form:
        guuid = request.form["uuid"]
        user = Users.query.filter_by(uuid=guuid).first()
        if user is not None:
            if user.OTPSecret is not None:
                user.OTPSecret = None
                db.session.commit()
                flash(f"Totp of user {str(user.username)} has been deleted", "good")
                log.info(
                    f"Totp of user {str(user.username)} has been deleted by {str(current_user.username)}"
                )
                return "ok"
            else:
                return force_logout_user()
        else:
            return force_logout_user()
    else:
        return force_logout_user()
    return ""


@users_bp.route("/del_user", methods=["POST"])
@check_is_admin
def del_user():
    if "uuid" in request.form:
        guuid = request.form["uuid"]
        search = Users.query.filter_by(uuid=guuid).first()
        if search is not None:
            db.session.delete(search)
            db.session.commit()
            if user.role == "User":
                data = os.path.join(DATA_PATH, "data", guuid)
                quarantine = os.path.join(DATA_PATH, "quarantine", guuid)
                scan = os.path.join(DATA_PATH, "scan", guuid)
                if os.path.exists(data):
                    os.rmdirs(data)
                if os.path.exists(quarantine):
                    os.rmdirs(quarantine)
                if os.path.exists(scan):
                    os.rmdirs(scan)
            flash(f"The user {search.username} has been deleted", "good")
            log.info(
                f"The user {search.username} has been deleted by {str(current_user.username)}"
            )
            return "ok"
        else:
            return force_logout_user()
    else:
        return force_logout_user()


@users_bp.route("/able_user", methods=["POST"])
@check_is_admin
def able_user():
    if "uuid" in request.form:
        guuid = request.form["uuid"]
        search = Users.query.filter_by(uuid=guuid).first()
        if search is not None:
            if search.enable == 1:
                search.enable = 0
                flash(f"The user {search.username} has been disable", "good")
                log.info(
                    f"The user {str(search.username)} has been disable by {str(current_user.username)}"
                )
            elif search.enable == 0:
                search.enable = 1
                flash(f"The user {search.username} has been enable", "good")
                log.info(
                    f"The user {str(search.username)} has been enable by {str(current_user.username)}"
                )
            db.session.commit()
            return "ok"
        else:
            return force_logout_user()
    else:
        return force_logout_user()


@users_bp.route("/add_job", methods=["POST"])
def add_job():
    if "addJob" in request.form:
        job_name = request.form["addJob"]
        regJob = r"^[a-zA-Z0-9-_.+\s]{1,255}$"
        if re.match(regJob, job_name):
            job = Job.query.filter_by(name=job_name).all()
            if job == []:
                new_job = Job(name=job_name)
                db.session.add(new_job)
                db.session.commit()
                log.info(f"New job {job_name} had been add by {current_user.username}")
                flash("New job had been add.", "good")
                return "ok"
            else:
                return "Job already exists"
        else:
            return "Bad paddings"
    else:
        return force_logout_user()


@users_bp.route("/remove_job", methods=["POST"])
def remove_job():
    if "RemoveJob" in request.form:
        job_name = request.form["RemoveJob"]
        if str(job_name) != "Choose a job":
            if Users.query.filter(Users.job.has(name=job_name)).first() is None:
                job = Job.query.filter_by(name=job_name).first()
                db.session.delete(job)
                db.session.commit()
                log.info(f"The job {job_name} has been deleted by {current_user.username}")
                flash(f"The job {job_name} has been deleted", "good")
                return "ok"
            else:
                return "This job was link to a person"
        else:
            return "Please select a job to remove"
    else:
        return force_logout_user()


@users_bp.route("/renderPP_user/<ouuid>")
def render_o_PP(ouuid):
    user = Users.query.filter_by(uuid=ouuid).first()
    if user.picture is not None:
        renderPP_io = open(user.picture, "rb")
        mimeType = "image/" + renderPP_io.name.split(".")[-1]
        return (
            send_file(renderPP_io, mimetype=mimeType),
            200,
            {"Content-Type": mimeType},
        )
    return ""
