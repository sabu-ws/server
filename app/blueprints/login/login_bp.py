from flask import Blueprint, render_template, redirect, url_for, request, flash, g, jsonify, abort, send_file, session

from app import login_user, logout_user, login_required, current_user, bcrypt, db, socketio, emit, app

from app.utils import logging
from app.forms import LoginForm
from app.models import Users, Endpoint
from config import *

import pyotp

login_bp = Blueprint(
	"login",
	__name__,
	template_folder="templates"
	)

def check_user():
	if current_user.role == "Admin":
		return redirect(url_for("admin.manage_users"))
	elif current_user.role == "User":
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
			if user != None:
				if bcrypt.check_password_hash(user.password,form.password.data) :
					if user.OTPSecret != None:
						session["totp"] = True
						session["user"] = user.username
						login_user(user)
						return redirect(url_for("login.mfa"))
					else:
						login_user(user)
						return render_template("login.html",con="ok")
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
					login_user(user)
					del session["totp"]
					del session["user"]
					return render_template("login_totp.html",con="ok")
				else:
					return render_template("login_totp.html",con="ko")
		else:
			return redirect(url_for("login.login"))
	else:
		return redirect(url_for("login.login"))
	return render_template("login_totp.html")


@login_bp.route("/logout",methods=["GET"])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login.login'))