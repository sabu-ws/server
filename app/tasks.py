from config import *

import subprocess
import datetime
import os



CPU_TABLE = []
RAM_TABLE = []
NET_TABLE = []

def job1():
	global CPU_TABLE
	global RAM_TABLE

			# with scheduler.app.app_context():
	file = open("/tmp/mama","a")
	file.write(f"cpu : {str(CPU_TABLE)}\n")
	file.write(f"ram : {str(RAM_TABLE)}\n")
	file.close()


def readCPU():
	global CPU_TABLE
	build = {"x":"","y":0}
	build["x"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	script = os.path.join(SCRIPT_PATH,"get_cpu_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
	build["y"] = result
	CPU_TABLE.append(build)

def readRAM():
	global RAM_TABLE
	build = {"x":"","y":0}
	build["x"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	script = os.path.join(SCRIPT_PATH,"get_ram_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","").split(" ")[0]
	formating = int(result) / 1024 / 1024
	end_format = float(f"{formating:3.1f}")
	build["y"] = end_format
	RAM_TABLE.append(build)

def readDISK():
	return

def readNET():
	return