from config import *

from flask import Flask
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, disconnect, send, join_room, rooms, close_room
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

import string
import random
import os
import re
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "".join(random.choices(string.ascii_letters + string.digits, k=30))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+db_name
app.config["UPLOAD_FOLDER"] = ROOT_PATH
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=NB_REVERSE_PROXY, x_proto=NB_REVERSE_PROXY)


# CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

# flask bcrypt
bcrypt = Bcrypt(app)


# sqlalchemy database
db = SQLAlchemy()
from app.models import Users, Job
if not os.path.exists(os.path.join("instance",db_name)):
	db.init_app(app)
	with app.app_context():
		db.create_all()
		while True:
			passwordAdmin = "".join(random.choices(string.ascii_letters+string.digits+"@!:;,?./+-*",k=20))
			if re.match(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",passwordAdmin):
				set_job_admin = Job(name="Administrator")
				db.session.add(set_job_admin)
				db.session.commit()
				set_admin = Users(uuid=uuid.uuid4().__str__(),name="Admin",firstname="Admin", email="admin@sabu.fr", username="Admin", role="Admin", job=1)
				set_admin.set_password(passwordAdmin)
				db.session.add(set_admin)
				db.session.commit()
				print("The password 'Admin' was :")
				print(passwordAdmin)
				break
			print("bad gen password")
else:
	db.init_app(app)


# Migrate db
migrate = Migrate(app, db)


# login manager
from app.models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))



# socketio
socketio = SocketIO(app)

from app import views