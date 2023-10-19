from flask import Blueprint, render_template, redirect, url_for, request, g

from app import app
from app.utils import sizeof_fmt, logging
from app.func import detectUSB, ifscan
from app.models import USBlog
from werkzeug.utils import secure_filename
from config import *

from urllib.parse import unquote, quote
from datetime import datetime
import time
from io import BytesIO
import zipfile
import subprocess
import os

browser_bp = Blueprint(
	"browser",
	__name__,
	template_folder="templates"
	)


@browser_bp.route("/path/<path:MasterListDir>",methods=["GET"])
@browser_bp.route("/path",methods=["GET"])
def path(MasterListDir=""):
	get_state_log = USBlog.query.filter_by(state=True).all()
	if len(get_state_log) != 0 :
		g.hasScan = True
	else:
		g.hasScan = False

	joining = os.path.join(ROOT_PATH,MasterListDir)
	logging("browser",f"accessing to {joining}")
	cur_dir = "/"+MasterListDir
	if cur_dir=="/":
		cur_dir=""
	if os.path.isdir(joining):
		new_path = os.listdir(joining)
		list_items = [i for i in os.walk(joining)][0]
		items_dir=[]
		items_file=[]
		for i in list_items[1]:
			j=os.path.join(joining,i)
			creation_date = str(datetime.fromtimestamp(os.lstat(j).st_ctime)).split(".")[0]
			modification_date = str(datetime.fromtimestamp(os.lstat(j).st_mtime)).split(".")[0]
			size = sizeof_fmt(os.lstat(j).st_size)
			iq = quote(i)
			# make [nom_fichier,date_de_creation,date_modifer,taille_fichier]
			make = [i,creation_date,modification_date,size,iq]
			items_dir.append(make)
		for i in list_items[2]:
			j=os.path.join(joining,i)
			creation_date = str(datetime.fromtimestamp(os.lstat(j).st_ctime)).split(".")[0]
			modification_date = str(datetime.fromtimestamp(os.lstat(j).st_mtime)).split(".")[0]
			size = sizeof_fmt(os.lstat(j).st_size)
			iq = quote(i)
			# make [nom_fichier,date_de_creation,date_modifer,taille_fichier]
			make = [i,creation_date,modification_date,size,iq]
			items_file.append(make)
		return render_template("browser_index.html",items_file=items_file,items_dir=items_dir,cur_dir=cur_dir)
	return redirect(url_for("browser.path"))

@browser_bp.route("/download/<path:MasterListDir>",methods=["POST"])
@detectUSB
@ifscan
def download(MasterListDir=""):
	if g.detectusb:
		path=ROOT_PATH+"/"+MasterListDir
		master_path="/".join(path.split("/")[:-1])
		last=MasterListDir.split("/")[-1]
		os.chdir(master_path)
		if os.path.exists(path):
			if os.path.isdir(path):
				timestr = time.strftime("%Y%m%d-%H%M%S")
				fileName = f"{last}_{timestr}.zip".format(timestr)
				memory_file = BytesIO()
				with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
					for root, dirs, files in os.walk(last):
						for file in files:
							zipf.write(os.path.join(root, file))
				memory_file.seek(0)
				logging("browser",f"downloading folder of [{path}]")
				return send_file(memory_file,as_attachment=True,mimetype="application/zip",download_name=fileName)
			elif os.path.isfile(path): 
				logging("browser",f"downloading file of [{path}]")
				return send_file(path,as_attachment=True)
		else:
			return redirect("/404")


@browser_bp.route("/upload/file",methods=["POST"])
@detectUSB
def upload_file():
	if g.detectusb:
		last = "/".join(request.referrer.split("/")[5:])
		master_path = os.path.join(ROOT_PATH,last)
		master_path = unquote(master_path)
		file = request.files["file"]
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(master_path, filename))
			logging("browser",f"file [{master_path}] is upload")
			return redirect(request.referrer)
	return("/404")




@browser_bp.route("/upload/folder",methods=["POST"])
@detectUSB
def upload_folder():
	if g.detectusb:
		last = "/".join(request.referrer.split("/")[5:])
		master_path = os.path.join(ROOT_PATH,last)
		master_path = unquote(master_path)
		for file in request.files.getlist('folder[]'):
			split_in_folder = file.filename.split("/")
			if len(split_in_folder) > 15 or "" in split_in_folder or ".." in split_in_folder or "%" in split_in_folder:
				flash("bad upload folder")
				return redirect(url_for("browser.path"))
			folder_creation = "/".join(i for i in split_in_folder[:-1])
			if not os.path.exists(os.path.join(master_path,folder_creation)):
				os.makedirs(os.path.join(master_path,folder_creation))
				logging("browser",f"new folder was created [{folder_creation}]")
			file.save(os.path.join(app.config["UPLOAD_FOLDER"],file.filename))
		folder_top_name = split_in_folder[0] 
		logging("browser",f"folder [{folder_top_name}] is upload")
		return redirect(request.referrer)
	return "/404"

@browser_bp.route("/delete/<path:MasterListDir>",methods=["GET"])
@detectUSB
def delete(MasterListDir=""):
	if g.detectusb:
		path=os.path.join(ROOT_PATH,MasterListDir)
		master_path="/".join(path.split("/")[:-1])
		last=MasterListDir.split("/")[-1]
		to_return = request.referrer
		os.chdir(master_path)
		if os.path.exists(path):
			if os.path.isdir(path):
				for root, dirs, files in os.walk(last, topdown=False):
					for name in files:
						os.remove(os.path.join(root, name))
					for name in dirs:
						os.rmdir(os.path.join(root, name))
				os.rmdir(last)
				logging("browser",f"deleting folder of [{path}]")
				return redirect(to_return)
			elif os.path.isfile(path):
				os.remove(last) 
				logging("browser",f"deleting file of [{path}]")
				return redirect(to_return)
		else:
			return redirect("/404")
	else:
		return redirect("/")


@browser_bp.route("/info/<path:MasterListDir>",methods=["GET"])
@detectUSB
def info(MasterListDir=""):
	if g.detectusb:
		path=ROOT_PATH+MasterListDir
		path = os.path.join(ROOT_PATH+MasterListDir)
		path = unquote(path)
		sub = subprocess.Popen(["exiftool",path],stdout=subprocess.PIPE).communicate()[0].decode().split("\n")
		logging("browser",f"get info of [{path}]")
		return render_template("browser_info.html",info=sub)
	else:
		return redirect("/")