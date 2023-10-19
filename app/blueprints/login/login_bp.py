from flask import Blueprint, render_template, redirect, url_for, request, flash, g, jsonify, abort, send_file, session

from app import login_user, logout_user, login_required, current_user, bcrypt, db, socketio, emit, app

from app.utils import logging
from app.forms import LoginForm
from app.models import Users, Endpoint
from config import *

import pyotp
import io
import qrcode

login_bp = Blueprint(
	"login",
	__name__,
	template_folder="templates"
	)

def check_user():
	if current_user.role == "admin":
		return "return to admin dashboard"
		return redirect(url_for("admin.dashboard"))
	elif current_user.role == "user":
		return "return to browser"
		return redirect(url_for("browser.path"))
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


# ============== à supprimer


@login_bp.route("/reg")
def reg():
	set_admin_user = Users(username="admin",role="admin")
	set_admin_user.set_password("P4$$w0rdF0r54Bu5t4t10N")
	db.session.add(set_admin_user)
	db.session.commit()
	return "ok"

@login_bp.route("/reg2")
def reg3():
	set_admin_user = Users(username="user",role="user",OTPSecret=pyotp.random_base32())
	set_admin_user.set_password("P4$$w0rdF0r54Bu5t4t10N")
	db.session.add(set_admin_user)
	db.session.commit()
	return "ok"

@login_bp.route("/render")
@login_required
def render():
	return render_template("render.html")

@login_bp.route("/render_qrcode")
@login_required
def qrcoderender():
	username = current_user.username
	totpsec = current_user.OTPSecret
	qr_code_url = pyotp.totp.TOTP(totpsec).provisioning_uri(name=username, issuer_name='SABU')
	img = qrcode.make(qr_code_url)
	buffer = io.BytesIO()
	img.save(buffer, format='PNG')
	buffer.seek(0)
	return send_file(buffer, mimetype='image/png'),200, {
        'Content-Type': 'image/png',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

import jwt
@login_bp.route("/newep")
def newep():
	if Endpoint.query.filter_by(hostname="ep1").first() is not True:
		token = jwt.encode({"hostname":"ep1"},"mysecret","HS256")
		set_new_ep = Endpoint(hostname="ep1",token=token,state=0,ip="127.0.0.1")
		db.session.add(set_new_ep)
		db.session.commit()
		return token

@login_bp.route("/shep")
def shep():
	a = Endpoint.query.filter_by(hostname="ep1").first()
	if a is not True:	
		return str(a.__dict__)
	return "nooo"