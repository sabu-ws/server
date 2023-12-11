from config import *

from app import app
from app import db
from app.models import Metrics, Devices


import subprocess
import os

log = app.logger

def read_CPU():
	with app.app_context():
		script = os.path.join(SCRIPT_PATH,"get_cpu_space.sh")
		result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
		get_device = Devices.query.filter_by(token="server").first()
		add_metrics = Metrics(name="cpu",value=int(result),idDevice=get_device.id)
		db.session.add(add_metrics)
		db.session.commit()
	
def read_RAM():
	with app.app_context():
		script = os.path.join(SCRIPT_PATH,"get_ram_space.sh")
		result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","").split(" ")[0]
		get_device = Devices.query.filter_by(token="server").first()
		add_metrics = Metrics(name="ram",value=int(result),idDevice=get_device.id)
		db.session.add(add_metrics)
		db.session.commit()
	