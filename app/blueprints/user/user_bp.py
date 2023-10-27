from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import qrcode
import pyotp
import io
import os

from app import login_required, logout_user ,current_user, bcrypt, login_user, db

from app.models import Users
from app.forms import AddUserForm
from config import *

user_bp = Blueprint(
	"user",
	__name__,
	template_folder="templates"
	)

totpsec = None

@user_bp.route("/")
@login_required
def index():
	user=Users.query.filter_by(id=current_user.id).first()
	return render_template("profil-settings.html",user=user)

# modify info
@user_bp.route("/mod_info",methods=["POST"])
@login_required
def mod_info():
	form = AddUserForm(data=request.form)
	if form.name.validate(form) and form.firstname.validate(form) and form.email.validate(form):
		user = Users.query.filter_by(id=current_user.id).first()
		user.name = form.name.data
		user.firstname = form.firstname.data
		user.email = form.email.data
		db.session.commit()
		flash("Your informations has been change!","good")
	else:
		flash(form.errors[list(form.errors.keys())[0]][0],"error")
	return redirect(url_for("user.index"))

# change password
@user_bp.route("/change_password",methods=["POST"])
@login_required
def change_password():
	user = Users.query.filter_by(id=current_user.id).first()
	current_password = request.form["currentPassword"]
	new_password = request.form["newPassword"]
	repeat_new_password = request.form["RepeatNewPassword"]
	if bcrypt.check_password_hash(user.password,current_password):
		if current_password != new_password:
			if new_password == repeat_new_password:
				data = {"password":repeat_new_password}
				if AddUserForm(data=data).password.validate(data):
					user.set_password(repeat_new_password)
					db.session.commit()
					flash("Your password has been change","good")
				else:
					flash("Bad paddings for new passwords","error")
			else:
				flash("New password and repeat password is not same","error")
		else:
			flash("Current password is same that new password","error")
	else:
		flash("Bad current password","error")
	return redirect(url_for("user.index"))


# totp / 2fa
@user_bp.route("/make_otp")
@login_required
def totpmake():
	global totpsec
	user = Users.query.filter_by(id=current_user.id).first()
	if user.OTPSecret == None:
		totpsec = pyotp.random_base32()
		return pyotp.totp.TOTP(totpsec).provisioning_uri(name=user.username, issuer_name='SABU')

@user_bp.route("/render_qrcode")
@login_required
def qrcoderender():
	global totpsec
	user = Users.query.filter_by(id=current_user.id).first()
	if "url" in request.args:
		url = request.args['url']
	if url != "":
		qr_code_url = url
		img = qrcode.make(qr_code_url)
		buffer = io.BytesIO()
		img.save(buffer, format='PNG')
		buffer.seek(0)
		return send_file(buffer, mimetype='image/png'),200, {
			'Content-Type': 'image/png',
			'Cache-Control': 'no-cache, no-store, must-revalidate',
			'Pragma': 'no-cache',
			'Expires': '0'}

@user_bp.route("/check_otp",methods=["POST"])
@login_required
def totpcheck():
	global totpsec
	if totpsec != None:
		if pyotp.TOTP(totpsec).verify(request.form["TestCode"]):
			user = Users.query.filter_by(id=current_user.id).first()
			user.OTPSecret = totpsec
			db.session.commit()
			flash("You have enable 2FA","good")
			return "ok"
		else:
			return "Bad totp code"

@user_bp.route("/disable_otp",methods=["POST"])
@login_required
def totpdisable():
	user = Users.query.filter_by(id=current_user.id).first()
	if user.OTPSecret != None:
		user.OTPSecret = None
		db.session.commit()
		flash("You have disable 2FA","good")
	return redirect(url_for('user.index'))


# Profile picture
@user_bp.route("/send_picture",methods=["POST"])
@login_required
def sendPicture():
	user = Users.query.filter_by(id=current_user.id).first()
	allowed_ext = ["image/png","image/jpg","image/jpeg"]
	if "filePP" in request.files:
		if not os.path.exists("ProfilePicture"):
			os.makedirs("ProfilePicture")
		file = request.files["filePP"]
		if file.content_type in allowed_ext:
			image = Image.open(file)
			px, py = image.size
			guuid = user.uuid
			filename =  guuid +"."+ file.content_type.split("/")[1]
			MAX_SIZE = 100 * 1024
			if len(file.read()) <= MAX_SIZE:
				if px <= 400 and py <= 400:
					path = os.path.join("ProfilePicture",filename)
					image.save(path)
					user.picture = path
					db.session.commit()
					flash("Your profile picture has been change","good")
				else:
					flash("Your image must did 400x400","error")
			else:
				flash("You image must be less than 100 KB")
		else:
			flash("Your picture must be to format png or jpg","error")
		return redirect(url_for("user.index")) 
	else:
		logout_user()

@user_bp.route("/renderPP")
@login_required
def renderPP():
	user = Users.query.filter_by(id=current_user.id).first()
	if user.picture != None:
		renderPP_io = open(user.picture,"rb")
		mimeType = "image/"+renderPP_io.name.split(".")[-1]
		return send_file(renderPP_io, mimetype=mimeType),200, {
			'Content-Type': mimeType,
			}		

	return ""