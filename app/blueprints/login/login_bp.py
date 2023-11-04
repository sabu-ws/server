from flask import Blueprint, render_template, redirect, url_for, request, flash, g, jsonify, abort, send_file, session

from app import login_user, logout_user, login_required, current_user, bcrypt, db, socketio, emit, app

from app.utils import logging
from app.forms import LoginForm
from app.models import Users, Job
from config import *

import pyotp

login_bp = Blueprint(
	"login",
	__name__,
	template_folder="templates"
	)

def check_user():
	if current_user.role == "Admin":
		session["job"] = Job.query.filter_by(id=current_user.job).first().name
		return redirect(url_for("panel.users.index"))
	elif current_user.role == "User":
		session["job"] = Job.query.filter_by(id=current_user.job).first().name
		return redirect(url_for("browser.index"))
	else:
		abort(404)

@login_bp.route("/",methods=["GET","POST"])
def login():
	session["totp"] = False
	if current_user.is_authenticated == True:
		return check_user()
	if request.method == "POST":
		data = dict(request.form)
		form = LoginForm(data=data)
		if form.password.validate(form):
			user = Users.query.filter_by(username=form.username.data).first()
			if user.enable == 1:
				if user != None:
					if bcrypt.check_password_hash(user.password,form.password.data) :
						session["user"] = user.username
						if user.OTPSecret != None:
							session["totp"] = True
							return redirect(url_for("login.mfa"))
						elif user.firstCon == 0 :
							return redirect(url_for('login.first_con'))
						else:
							session["job"] = Job.query.filter_by(id=user.job).first().name 
							del session["totp"]
							login_user(user)
							return render_template("login.html",con="ok")
					else:
						return render_template("login.html",con="ko")
				else:
					return render_template("login.html",con="ko")
			else:
				return render_template("login.html",con="ko")
		return render_template("login.html",con="ko")
	return render_template("login.html")

@login_bp.route("/mfa",methods=["GET","POST"])
def mfa():
	if "totp" in session:
		if session["totp"] == True:
			if request.method=="POST":
				data = dict(request.form)
				user = Users.query.filter_by(username=session["user"]).first()
				totp = pyotp.TOTP(user.OTPSecret)
				if totp.verify(data["totp"]):
					del session["totp"]
					session["job"] = Job.query.filter_by(id=user.job).first().name 
					login_user(user)
					return render_template("login_totp.html",con="ok")
				else:
					return render_template("login_totp.html",con="ko")
		else:
			return redirect(url_for("login.login"))
	else:
		return redirect(url_for("login.login"))
	return render_template("login_totp.html")


@login_bp.route("/first_connection",methods=["GET","POST"])
def first_con():
	if "user" in session:
		if current_user.is_authenticated == True:
			return check_user()
		get_user = Users.query.filter_by(username=session['user']).first()
		if request.method == "POST":
			data = request.form
			if "newPasswordInput" in data and "repeatPasswordInput" in data:
				if data["newPasswordInput"] == data["repeatPasswordInput"]:
					dataf={"username":session['user'],"password":data["newPasswordInput"]}
					form = LoginForm(data=dataf)
					if form.validate():
						get_user.firstCon = 1
						db.session.commit()
						session["job"] = Job.query.filter_by(id=get_user.job).first().name
						login_user(get_user)
						return render_template("login_first_con.html",con="ok")
					else:
						return render_template("login_first_con.html",con="ko",error=form.errors["password"][0])
				else:
					return render_template("login_first_con.html",con="ko",error="The password fields are not the same.")
			else:
				return redirect(url_for('login.login'))
	else:
		return redirect(url_for('login.login'))
	return render_template("login_first_con.html")

@login_bp.route("/logout",methods=["GET"])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login.login'))
