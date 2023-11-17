from config import *
import os
import subprocess
import random
# from app import scheduler

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
	script = os.path.join(SCRIPT_PATH,"get_cpu_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
	CPU_TABLE.append(result)

def readRAM():
	global RAM_TABLE
	script = os.path.join(SCRIPT_PATH,"get_ram_space.sh")
	result = subprocess.Popen(["bash",script],stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","").split(" ")[0]
	RAM_TABLE.append(result)

def readDISK():
	return

def readNET():
	return