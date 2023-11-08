from flask import Blueprint, request, jsonify
from functools import wraps

from app import socketio, emit, disconnect, send, join_room, rooms, close_room, db, login_user, login_required, current_user, logout_user, bcrypt

from app.utils import logging
from app.models import Endpoint, Users
from config import *

import pyotp

api_bp = Blueprint(
	"api",
	__name__,
	template_folder="templates"
	)


# ==================== controller api
def check_headers(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if "X-SABUAPITOKEN" in request.headers and "X-SABUHOSTNAME" in request.headers:
			if Endpoint.query.filter_by(hostname=request.headers["X-SABUHOSTNAME"],token=request.headers["X-SABUAPITOKEN"]).first():
				return f(*args, **kwargs)
			else:
				print("error")
		else:
			print("error")
	return decorated_function

def check_room(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		get_rooms = rooms(namespace="/api/v2", sid=request.sid)
		if request.headers["X-SABUHOSTNAME"] in get_rooms:
			return f(*args, **kwargs)
	return decorated_function

# ==================== controller api


# =================== basic websocket function

@socketio.on("join",namespace='/api/v2')
@check_headers
def join(*args,**kwargs):
	join_room(request.headers["X-SABUHOSTNAME"],namespace='/api/v2',sid=request.sid)
	set_state = Endpoint.query.filter_by(hostname=request.headers["X-SABUHOSTNAME"]).first()
	set_state.state = 1
	db.session.commit()
	print("new client join room")

@socketio.on("connect",namespace='/api/v2')
def connect(data):
	print("new client connected sid :",request.sid, request.remote_addr)

@socketio.on("disconnect",namespace='/api/v2')
def discconnect():
	get_rooms = rooms(namespace="/api/v2",sid=request.sid)
	if request.headers["X-SABUHOSTNAME"] in get_rooms:
		close_room(request.headers["X-SABUHOSTNAME"],namespace="/api/v2")
		set_state = Endpoint.query.filter_by(hostname=request.headers["X-SABUHOSTNAME"]).first()
		set_state.state = 0
		db.session.commit()
		print("room close ",get_rooms[0])
	print("client was deconnected sid : ",request.sid)

# =================== basic websocket function


# =============================== Start API ===============================

@socketio.on("ping",namespace='/api/v2')
@check_room
def ping(*args,**kwargs):
	emit("ping","pong",namespace='/api/v2',sid=request.sid)


@socketio.on("set_connection",namespace='/api/v2')
@check_room
def set_connect(data):
	user = Users.query.filter_by(username=data["username"]).first()
	if user is None:
		emit("callback",{"error":"user not found1"},namespace="/api/v2",to=request.headers["X-SABUHOSTNAME"])
	else:
		if bcrypt.check_password_hash(user.password,data["password"]):
			if user.OTPSecret is None:
				login_user(user)
				emit("callback",{"message":"user connected","user":user.username},namespace="/api/v2",to=request.headers["X-SABUHOSTNAME"])
			else:
				emit("callback",{"error":"need otp"},namespace="/api/v2",to=request.headers["X-SABUHOSTNAME"])
		else:
			emit("callback",{"error":"user not found2"},namespace="/api/v2",to=request.headers["X-SABUHOSTNAME"])

@socketio.on("check_otp",namespace="/api/v2")
def check_otp(data):
	print(data)
	user = Users.query.filter_by(username=data["username"]).first()
	if user == None:
		emit("callback", {"error":"bad credentials"}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])
	else:
		if bcrypt.check_password_hash(user.password, data["password"]):
			if user.OTPSecret is None:
				emit("callback", {"error":"bad credentials"}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])
			else:
				totp = pyotp.TOTP(user.OTPSecret)
				if totp.verify(data["totp"]):
					login_user(user)
					emit("callback", {"message":"user connected", "user":user.username}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])
				else:
					emit("callback", {"error":"bad otp"}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])
		else:
			emit("callback", {"error":"bad credentials"}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])


@socketio.on("show_connection",namespace="/api/v2")
@check_room
def show_con():
	emit("callback", {"message":current_user.is_authenticated}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])


@socketio.on("set_disconnection",namespace="/api/v2")
@check_room
def dis_con():
	logout_user()
	emit("callback", {"message":"user deconnected"}, namespace="/api/v2", to=request.headers["X-SABUHOSTNAME"])


@api_bp.route("/emit")
def emitsomething():
	emit("ping", "pong", namespace='/api/v2', broadcast=True)
	return request.remote_addr
