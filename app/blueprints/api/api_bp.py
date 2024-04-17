from config import *

from app import (
    socketio,
    db,
    cache,
    login_user,
    current_user,
    logout_user,
    bcrypt,
    logger as log,
    apiws,
    csrf
)
from app.models import Devices, Users

from flask_socketio import emit, join_room, rooms, close_room
from flask import Blueprint, request, session, jsonify
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
                    log.info(
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
    log.info(str(request.sid))
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
    log.info(str(request.sid))
    if "username" in data and "code" in data:
        user = Users.query.filter(Users.username==data["username"] and Users.role=="User").first()
        if user is None:
            emit(
                "callback",
                {"error": "bad credentials"},
                namespace="/api/v2",
                to=request.headers["X-SABUHOSTNAME"],
            )
            hostname = str(request.headers["X-SABUHOSTNAME"])
            username = str(data["username"])
            log.info(f"Endpoint {hostname} enter bad username : {username}")
        else:
            key_user = f"codeEP_{str(user.uuid)}"
            data_code_user = cache.get(key_user)
            if data_code_user is not None:
                if data_code_user == data["code"]:
                    emit(
                        "callback",
                        {"message": "user connected"},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
                    login_user(user)
                    session["username"] = user.username
                    hostname = str(request.headers["X-SABUHOSTNAME"])
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} connect a username : {username}")
                else:
                    emit(
                        "callback",
                        {"error": "bad credentials"},
                        namespace="/api/v2",
                        to=request.headers["X-SABUHOSTNAME"],
                    )
                    hostname = str(request.headers["X-SABUHOSTNAME"])
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} enter bad code : {username}")
            else:
                emit(
                    "callback",
                    {"error": "bad credentials"},
                    namespace="/api/v2",
                    to=request.headers["X-SABUHOSTNAME"],
                )
                hostname = str(request.headers["X-SABUHOSTNAME"])
                username = str(data["username"])
                log.info(f"Endpoint {hostname} enter bad username : {username}")

@api_bp.route("/status_user")
def status_user():
    msg = "disconnected"
    info = {}
    if current_user.is_authenticated:
        msg = "connected"
        info = {
            "username": current_user.username,
            "name": current_user.name,
            "firstname":current_user.firstname,
            "job":current_user.job.name
        }
    data = {"message": msg,"info": info}
    return jsonify(data) 

@api_bp.route("/set_connection",methods=["POST","GET"])
@check_headers
@csrf.exempt
def set_connection():
    get_hostname = request.headers["X-SABUHOSTNAME"]
    get_device = Devices.query.filter_by(
        hostname=get_hostname
    ).first()
    data = request.form
    if get_device.state == 1:
        if "username" in data and "code" in data:
            user = Users.query.filter(Users.username==data["username"] and Users.role=="User").first()
            if user is None:
                hostname = str(get_hostname)
                username = str(data["username"])
                log.info(f"Endpoint {hostname} enter bad username : {username}")
                return jsonify({"error": "bad credentials"})
            else:
                key_user = f"codeEP_{str(user.uuid)}"
                data_code_user = cache.get(key_user)
                if data_code_user!=None:
                    if data_code_user == data["code"]:
                        login_user(user)
                        session["username"] = user.username
                        hostname = str(get_hostname)
                        username = str(data["username"])
                        log.info(f"Endpoint {hostname} connect a username : {username}")
                        return jsonify({"message": "user connected"})
                    else:
                        hostname = str(get_hostname)
                        username = str(data["username"])
                        log.info(f"Endpoint {hostname} enter bad code : {username}")
                        return jsonify({"error": "bad credentials"})
                else:
                    hostname = str(get_hostname)
                    username = str(data["username"])
                    log.info(f"Endpoint {hostname} enter bad username : {username}")
                    return jsonify({"error": "bad credentials"})

@api_bp.route("/set_deconnection",methods=["POST","GET"])
@check_headers
@csrf.exempt
def set_deconnection():
    logout_user()
    return jsonify({"message": "user deconnected"})