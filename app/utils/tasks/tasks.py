from config import *

import subprocess
import datetime
import os

CPU_TABLE = []
RAM_TABLE = []
NET_TABLE = []


def read_CPU():
	global CPU_TABLE
	build = {"x":"","y":0}
	build["x"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	script = os.path.join(SCRIPT_PATH,"get_cpu_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
	build["y"] = result
	CPU_TABLE.append(build)

def read_RAM():
	global RAM_TABLE
	build = {"x":"","y":0}
	build["x"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	script = os.path.join(SCRIPT_PATH,"get_ram_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","").split(" ")[0]
	formating = int(result) / 1024 / 1024
	end_format = float(f"{formating:3.1f}")
	build["y"] = end_format
	RAM_TABLE.append(build)