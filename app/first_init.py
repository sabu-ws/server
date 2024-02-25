from config import *
from app import app, db, logger as log
from app.models import Users, Devices, Job, Extensions, Setup
from app.utils.system import SYS_get_hostname
from app.utils.db_mgmt import database_allowed

from sqlalchemy import text
import subprocess
import csv
import os

def database_init():
    log.info("Initialisation database")
    with app.app_context():
        pg_add_extension()
        db.create_all()
        db.session.commit()

        # log.info("Load stamp migration in database")
        # stamp_migration()

        create_admin_job()

        create_admin_user()

        create_server_device()

        pg_add_hypertable()

        add_mimetype_extention()

        setup_maintenance()
        
        check_data_folder()
    
        end_intallation()
        # log.info("Upgrade database if need")
        # upgrade_migration()

def create_admin_user():
    if Users.query.filter_by(username="admin").first() is None:
        log.info("Create admin user")
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
    if Job.query.filter_by(name="Administrator").first() is None:
        log.info("Create Administrator job")
        set_job_admin = Job(name="Administrator")
        db.session.add(set_job_admin)
        db.session.commit()
    return None


def create_server_device():
    if Devices.query.filter_by(token="server").first() is None:
        log.info("Create server device")
        set_device_server = Devices(
            hostname=SYS_get_hostname(),
            description="This is the master server",
            token="server",
            state=1,
        )
        db.session.add(set_device_server)
        db.session.commit()
    return None


def pg_add_extension():
    if "postgresql" == database_allowed()[:10]:
        with db.engine.connect() as con:
            con.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
            con.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))
            con.commit()


def pg_add_hypertable():
    with db.engine.connect() as con:
        con.execute(
           text(   
               "SELECT create_hypertable('metrics', by_range('timestamp_ht', INTERVAL '24 hours'),migrate_data => true, if_not_exists => true);"
           )
        )
        con.execute(
            text(
                "SELECT add_retention_policy('metrics', INTERVAL '7 days',if_not_exists => true);"
            )
        )
        con.commit()

def add_mimetype_extention():
    if Extensions.query.count() == 0:
        with open("mime.csv","r") as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for ext_mime in reader:
                extension_row = Extensions(
                    extension=ext_mime[0],
                    mimetype=ext_mime[1]
                )
                db.session.add(extension_row)
                db.session.commit()
    return 

def setup_maintenance():
    if Setup.query.filter_by(action="ret").first() == None:
        ret = Setup(action="ret",value="30")
        db.session.add(ret)
        db.session.commit()
    if Setup.query.filter_by(action="appc").first() == None:
        appc = Setup(action="appc",value="ED")
        db.session.add(appc)
        db.session.commit()
    if Setup.query.filter_by(action="appt").first() == None:
        appt = Setup(action="appt",value="02:00")
        db.session.add(appt)
        db.session.commit()

def check_data_folder():
    quarantine_path = "/sabu/data/quarantine"
    data_path = "/sabu/data/data"
    scan_path = "/sabu/data/scan"
    if not os.path.exists(quarantine_path):
        log.info("Creating to quarantine path")
        os.makedirs(quarantine_path)
    if not os.path.exists(data_path):
        log.info("Creating to data path")
        os.makedirs(data_path)
    if not os.path.exists(scan_path):
        log.info("Creating to scan path")
        os.makedirs(scan_path)
    return ""

def end_intallation():
    if Setup.query.filter_by(action="setup").first() == None:
        set_setup = Setup(action="setup",value="1")
        db.session.add(set_setup)
        db.session.commit()
        subprocess.Popen(["sudo","/usr/bin/systemctl","restart","sabu.service"])