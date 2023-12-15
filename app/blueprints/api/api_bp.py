from config import *

from app import (
    socketio,
    db,
    login_user,
    current_user,
    logout_user,
    bcrypt,
    logger as log,
)
from app.models import Devices, Users

from flask_socketio import emit, join_room, rooms, close_room
from flask import Blueprint, request
from functools import wraps
import pyotp
import jwt

api_bp = Blueprint("api", __name__, template_folder="templates")


# ==================== controller api
def check_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "X-SABUAPITOKEN" in request.headers and "X-SABUHOSTNAME" in request.headers:
            get_device_token = Devices.query.filter_by(
                hostname=request.headers["X-SABUHOSTNAME"]
            ).first()
            if get_device_token:
                token = get_device_token.token
                try:
                    data = jwt.decode(
                        request.headers["X-SABUAPITOKEN"], token, algorithms=["HS256"]
                    )
                    return f(*args, **kwargs)
                except jwt.ExpiredSignatureError:
                    log.info(
                        f"Endpoint {str(get_device_token.hostname)} has expire signature"
                    )
                except jwt.InvalidSignatureError:
                    print(
                        f"Endpoint {str(get_device_token.hostname)} enter bad signature"
                    )
            else:
                log.info("Someone try to connect without good headers")
        else:
            log.info("Someone try to connect without good headers")

    return decorated_function


def check_room(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "X-SABUHOSTNAME" in request.headers:
            get_rooms = rooms(namespace="/api/v2", sid=request.sid)
            if request.headers["X-SABUHOSTNAME"] in get_rooms:
                return f(*args, **kwargs)

    return decorated_function


# ==================== controller api


# =================== basic websocket function


@socketio.on("join", namespace="/api/v2")
@check_headers
def join(*args, **kwargs):
    join_room(request.headers["X-SABUHOSTNAME"], namespace="/api/v2", sid=request.sid)
    device = Devices.query.filter_by(hostname=request.headers["X-SABUHOSTNAME"]).first()
    socketio.emit(
        "state", {"state": "up", "uuid": str(device.uuid)}, namespace="/state_ep"
    )
    log.info(
        f"Endpoint {str(device.hostname)} is connected and join a room {str(request.remote_addr)}"
    )
    device.state = 1
    db.session.commit()


@socketio.on("connect", namespace="/api/v2")
def connect(data):
    print("New client connected sid :", request.sid, request.remote_addr)


@socketio.on("disconnect", namespace="/api/v2")
def discconnect():
    get_rooms = rooms(namespace="/api/v2", sid=request.sid)
    if "X-SABUHOSTNAME" in request.headers:
        if request.headers["X-SABUHOSTNAME"] in get_rooms:
            close_room(request.headers["X-SABUHOSTNAME"], namespace="/api/v2")
            device = Devices.query.filter_by(
                hostname=request.headers["X-SABUHOSTNAME"]
            ).first()
            device.state = 0
            socketio.emit(
                "state",
                {"state": "down", "uuid": str(device.uuid)},
                namespace="/state_ep",
            )
            log.info(f"Endpoint {str(device.hostname)} is disconnected")
            db.session.commit()
    if current_user.is_authenticated:
        logout_user()


# =================== basic websocket function


# =============================== Start API ===============================


@socketio.on("ping", namespace="/api/v2")
@check_room
def ping(*args, **kwargs):
    emit("ping", "pong", namespace="/api/v2", sid=request.sid)


@socketio.on("set_connection", namespace="/api/v2")
@check_room
def set_connect(data):
    if "username" in data and "password" in data:
        user = Users.query.filter_by(username=data["username"]).first()
        if user is None:
            emit(
                "callback",
                {"error": "user not found"},
                namespace="/api/v2",
                to=request.headers["X-SABUHOSTNAME"],
            )
            hostname = str(request.headers["X-SABUHOSTNAME"])
            username = str(data["username"])
            log.info(f"Endpoint {hostname} enter bad username : {username}")
        else:
            if bcrypt.check_password_hash(user.password, data["password"]):
                if user.OTPSecret is None:
                    login_user(user)
                    emit(
                        "callback",
                        {"message": "user connected", "user": user.username},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
                    hostname = str(request.headers["X-SABUHOSTNAME"])
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} connect a username : {username}")
                else:
                    emit(
                        "callback",
                        {"error": "need otp"},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
            else:
                emit(
                    "callback",
                    {"error": "user not found"},
                    namespace="/api/v2",
                    to=request.headers["X-SABUHOSTNAME"],
                )
                hostname = str(request.headers["X-SABUHOSTNAME"])
                username = str(data["username"])
                log.info(f"Endpoint {hostname} enter bad password : {username}")


@socketio.on("check_otp", namespace="/api/v2")
@check_room
def check_otp(data):
    user = Users.query.filter_by(username=data["username"]).first()
    hostname = str(request.headers["X-SABUHOSTNAME"])
    if user == None:
        emit(
            "callback",
            {"error": "bad credentials"},
            namespace="/api/v2",
            to=request.headers["X-SABUHOSTNAME"],
        )
        username = str(data["username"])
        log.info(f"Endpoint {hostname} enter bad username : {username}")
    else:
        if bcrypt.check_password_hash(user.password, data["password"]):
            if user.OTPSecret is None:
                emit(
                    "callback",
                    {"error": "bad credentials"},
                    namespace="/api/v2",
                    to=request.headers["X-SABUHOSTNAME"],
                )
                username = str(data["username"])
                log.info(f"Endpoint {hostname} get no totp for a user : {username}")
            else:
                totp = pyotp.TOTP(user.OTPSecret)
                if totp.verify(data["totp"]):
                    login_user(user)
                    emit(
                        "callback",
                        {"message": "user connected", "user": user.username},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} connect a username : {username}")
                else:
                    emit(
                        "callback",
                        {"error": "bad otp"},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} enter bad totp : {username}")
        else:
            emit(
                "callback",
                {"error": "bad credentials"},
                namespace="/api/v2",
                to=request.headers["X-SABUHOSTNAME"],
            )
            username = str(data["username"])
            log.info(f"Endpoint {hostname} enter bad password : {username}")


@socketio.on("show_connection", namespace="/api/v2")
@check_room
def show_con():
    msg = "user disconnected"
    if current_user.is_authenticated:
        msg = "user connected"
    emit(
        "callback",
        {"message": msg},
        namespace="/api/v2",
        to=request.headers["X-SABUHOSTNAME"],
    )


@socketio.on("set_disconnection", namespace="/api/v2")
@check_room
def dis_con():
    if current_user.is_authenticated:
        hostname = str(request.headers["X-SABUHOSTNAME"])
        username = str(current_user.username)
        emit(
            "callback",
            {"message": "user disconnected"},
            namespace="/api/v2",
            to=request.headers["X-SABUHOSTNAME"],
        )
        log.info(f"Endpoint {hostname} disconnect a username : {username}")
        logout_user()


@api_bp.route("/emit")
def emitsomething():
    emit("ping", "pong", namespace="/api/v2", broadcast=True)
    return request.remote_addr
