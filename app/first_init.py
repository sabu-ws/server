from config import *
from app import app, db
from app.models import Users, Devices, Job
from app.utils.system import NET_get_ip_server, SYS_get_hostname
from app.utils.db_mgmt import database_allowed
from app.utils.db_mgmt.migrate import stamp_migration, upgrade_migration

from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database
from sqlalchemy import create_engine
from sqlalchemy import URL

def database_init():
	url_object = database_allowed(app.root_path)
	engine = create_engine(url_object)
	if not database_exists(engine.url):
		engine.dispose()
		with app.app_context():
			db.create_all()
			stamp_migration()
			create_admin_job()
			create_admin_user()
			create_server_device()
	else:
		with app.app_context():
			upgrade_migration()

def create_admin_user():
	if Users.query.filter_by(username="admin").first() == None:
		set_admin = Users(
			name="SABU",
			firstname="Admin",
			email="admin@sabu.fr",
			username="admin",
			role="Admin",
			job_id=1,
		)
		set_admin.set_password("P4$$w0rdF0r54Bu5t4t10N")
		db.session.add(set_admin)
		db.session.commit()
	return None

def create_admin_job():
	if Job.query.filter_by(name="Administrator").first() == None :
		set_job_admin = Job(name="Administrator")
		db.session.add(set_job_admin)
		db.session.commit()
	return None

def create_server_device():
	if Devices.query.filter_by(token="server").first() == None:
		set_device_server = Devices(
			hostname=SYS_get_hostname(),
			description="This is the master server",
			token="server",
			state=1
			)
		db.session.add(set_device_server)
		db.session.commit()
	return None