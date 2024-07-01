from config import *
from app.utils.db_mgmt import database_allowed

from flask import Flask
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_socketio import (
    SocketIO,
    emit,
    disconnect,
)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect, CSRFError
from app.utils.api.api_session import ApiWS
from werkzeug.middleware.proxy_fix import ProxyFix

import datetime
import logging
import string
import random
import redis
import os
import re
import uuid

# log_format = '[%(levelname)s] %(asctime)s  %(message)s'
# logger = logging.getLogger("sabu.server")
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("/sabu/logs/server/sabu2.log")
# file_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


# log_format = '[%(levelname)s] %(asctime)s %(hostname)s (%(username)s) %(page)s %(action)s : %(message)s'
log_format = '[%(levelname)s] %(asctime)s  %(message)s'

logging.basicConfig(
    format= log_format,
    level=logging.DEBUG,
    filename="/sabu/logs/server/sabu2.log",
    filemode="a",
)
logger = logging.getLogger("sabu.server")
# logger = logging.LoggerAdapter(logger, {
    # 'hostname': "server",
    # 'username': "system",
    # 'page': 'index',
    # 'action': ''
# })

# class logger:
    # def info(msg):
        # return ""
    # def error(msg):
        # return ""
# logger.info('remove_old_files.sh completed successfully', extra={'username': 'mbinet', 'module': 'ENDPOINT', 'action': 'EXEC-SCRIPT'})
# logger.info('remove_old_files.sh completed successfully')

app = Flask(__name__)
app.config["SECRET_KEY"] = "".join(
    random.choices(string.ascii_letters + string.digits, k=30)
)
app.config["SQLALCHEMY_DATABASE_URI"] = database_allowed()
app.config["UPLOAD_FOLDER"] = ROOT_PATH
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Session configure with redis
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_KEY_PREFIX"] = "SABU_session_"
app.config["SESSION_COOKIE_SECURE"] = True
# redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT),db=int(REDIS_DB_CACHE), password=REDIS_PASSWORD)
redis_client = redis.Redis(
    host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB_CACHE)
)
app.config["SESSION_REDIS"] = redis_client
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=12)

# Cache config
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_KEY_PREFIX"] = "SABU_cache_"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
app.config["CACHE_REDIS_HOST"] = REDIS_HOST
app.config["CACHE_REDIS_PORT"] = REDIS_PORT
# app.config["CACHE_REDIS_PASSWORD"] = REDIS_PASSWORD
app.config["CACHE_REDIS_DB"] = int(REDIS_DB_CACHE)

# Celery config
redis_client_scanner_url = (
    f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{int(REDIS_PORT)}/{int(REDIS_DB_CELERY)}"
)
app.config["broker_url"] = redis_client_scanner_url
app.config["broker_connection_retry_on_startup"] = True
app.config["result_backend"] = redis_client_scanner_url
app.config["broker_transport"] = "redis"

# Proxy fix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=NB_REVERSE_PROXY, x_proto=NB_REVERSE_PROXY)

logger.info("Initialisation flask extensions")

# CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)


# flask bcrypt
bcrypt = Bcrypt(app)

# flask caching
cache = Cache(app)

# sqlalchemy database
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)


# login manager
from app.models import Users

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# socketio
socketio = SocketIO(app)


# Session manager
session = Session(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# API ws session
apiws = ApiWS(app, redis_client, key_prefix="SABU_api_")

# Import all views
from app import views
