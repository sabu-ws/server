from flask import Blueprint, render_template, redirect, request, flash, jsonify
import uuid
from sqlalchemy import or_
import re

from app import login_required, current_user, db, logout_user

from app.utils import logging
from app.forms import AddUserForm 
from app.models import Users, Job
from config import *

users_bp = Blueprint(
	"users",
	__name__
	)

@users_bp.before_request
def users_bp_before_request():
	if current_user.is_authenticated == False :
		return redirect(url_for("login.login"))

@users_bp.route("/")
def index():
	get_user_list = Users.query.all()
	get_job_name = db.session.query(Job.name).all()
	for user in get_user_list:
		user.job = Job.query.filter_by(id=user.job).first().name
	return render_template("ap_users.html",userList=get_user_list,job_list=get_job_name)


@users_bp.route("/add_user",methods=["POST"])
def add_user():
	data = request.form
	if data["password"] == data["AddRepeatPassword"]:
		if data["name"] and data["firstname"] and  data["username"] and data["password"] and data["role"] and data["email"] and data["job"]:
			form = AddUserForm(data=data)
			if data["job"] != "Choose a job":
				queryJob = Job.query.filter_by(name=data["job"]).first()
				if queryJob != None:
					if AddUserForm.validate(form):
						if Users.query.filter_by(username=data["username"]).first() == None:
							guuid = str(uuid.uuid4())
							useradd = Users(uuid=guuid,username=data["username"],name=data["name"],firstname=data["firstname"],role=data["role"],email=data["email"],job=queryJob.id,enable=1)
							useradd.set_password(data["password"])
							db.session.add(useradd)
							db.session.commit()
							flash(f"New user added {data['username']}","good")
							return "ok"
						else:
							return "This username already exists"
					else:
						keys = list(dict(form.errors.items()))
						return jsonify(dict(form.errors.items())[keys[0]][0])
				else:
					logout_user()
					return "ok"
			else:
				return "Please select a job"
		else:
			return "Please fields all input"
	else:
		return "Password fields are not the same "

@users_bp.route("/mod_user",methods=["POST"])
def mod_user():
	data = request.form
	form = AddUserForm(data=data)
	if "uuid" in request.form:
		guuid = request.form["uuid"]
		queryUser = Users.query.filter_by(uuid=guuid).first()
		if queryUser != None:
			if form.firstname.validate(form) and form.name.validate(form) and form.username.validate(form) and form.role.validate(form) and form.email.validate(form):
				job = data["job"]
				if job != "Choose a job":
					queryJob = Job.query.filter_by(name=job).first()
					if queryJob != None:
						if request.form["password"] != "" and request.form["EditRepeatPassword"] != "":
							if request.form["password"] == request.form["EditRepeatPassword"]:
								if form.password.validate(form):
									queryUser.password = data["password"]
								else:
									keys = list(dict(form.errors.items()))
									return dict(form.errors.items())[keys[0]][0]
							else:
								return "Password fields are not the same"
					else:
						logout_user()
						return redirect("/")
				else:
					return "Please select a job"
				queryUser.username = data["username"]
				queryUser.name = data["name"]
				queryUser.firstname = data["firstname"]
				queryUser.email = data["email"]
				queryUser.job = queryJob.id
				db.session.flush()
				db.session.commit()
				session["job"] = queryJob.name
				flash(f"The informations of {queryUser.username} have been change","good")
				return "ok"
			else:
				keys = list(dict(form.errors.items()))
				return jsonify(dict(form.errors.items())[keys[0]][0])
		else:
			logout_user()
			return redirect("/")
	else:
		logout_user()
		return redirect("/")
	return 

@users_bp.route("/mod_user/query",methods=["POST"])
def mod_user_query():
	if "uuid" in request.form:
		guuid = request.form["uuid"]
		user = Users.query.filter_by(uuid=guuid).first()
		if user != None:
			user.job = Job.query.filter_by(id=user.job).first().name
			return jsonify({"uuid":user.uuid,"name":user.name,"firstname":user.firstname,"username":user.username,"email":user.email,"job":user.job,"totp":True if user.OTPSecret else False,"role":user.role})
		else:
			logout_user()
			return ""
	else:
		logout_user()
		return ""

@users_bp.route("/mod_user/disable_otp",methods=["POST"])
def mod_user_disable_otp():
	if "uuid" in request.form:
		guuid = request.form["uuid"]
		user = Users.query.filter_by(uuid=guuid).first()
		if user != None:
			if user.OTPSecret != None:
				user.OTPSecret = None
				db.session.commit()
				return "ok"
			else:
				logout_user()
				return ""
		else:
			logout_user()
			return ""
	else:
		logout_user()
		return ""
	return ""

@users_bp.route("/del_user",methods=["POST"])
def del_user():
	if "uuid" in request.form:
		guuid = request.form["uuid"]
		search = Users.query.filter_by(uuid=guuid).first()
		if search != None:
			db.session.delete(search)
			db.session.commit()
			flash(f"The user {search.username} has been deleted","good")
			return "ok"
		else:
			logout_user()
			return "ok"
	else:
		logout_user()
		return "ok"

@users_bp.route("/able_user",methods=["POST"])
def able_user():
	if "uuid" in request.form:
		guuid = request.form["uuid"]
		search = Users.query.filter_by(uuid=guuid).first()
		if search != None:
			if search.enable == 1:
				search.enable = 0
				flash(f"The user {search.username} has been disable","good")
			elif search.enable == 0:
				search.enable = 1
				flash(f"The user {search.username} has been enable","good")
			db.session.commit()
			return "ok"
		else:
			logout_user()
			return "ok"
	else:
		logout_user()
		return "ok"

@users_bp.route("/add_job",methods=["POST"])
def add_job():
	if "addJob" in request.form:
		job_name = request.form["addJob"]
		regJob = r'^[a-zA-Z0-9-_.+\s]{1,255}$'
		if re.match(regJob,job_name):
			job = Job.query.filter_by(name=job_name).all()
			if job == []:
				new_job = Job(name=job_name)
				db.session.add(new_job)
				db.session.commit()
				flash("New job had been add.","good")
				return "ok"
			else:
				return "Job already exists"
		else:
			return "Bad paddings"
	else:
		logout_user()
		return "ok"

@users_bp.route("/remove_job",methods=["POST"])
def remove_job():
	if "RemoveJob" in request.form:
		job_name = request.form["RemoveJob"]
		if str(job_name) != "Choose a job":
			query_job = Job.query.filter_by(name=job_name).first()
			if query_job != None:
				if Users.query.filter_by(job=query_job.id).first()==None:
					job = Job.query.filter_by(name=job_name).first()
					db.session.delete(job)
					db.session.commit()
					flash(f"The job {job_name} has been deleted","good")
					return "ok"
				else:
					return "This job was link to a person"
			else:
				logout_user()
				return "ok"
		else:
			return "Please select a job to remove"
	else:
		logout_user()
		return "ok"