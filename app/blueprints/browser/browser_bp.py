from config import *
from flask import Blueprint, redirect, url_for, render_template, abort, session, send_file, request, flash, session, jsonify
from werkzeug.utils import secure_filename

from app import login_required, current_user, logout_user, logger as log, db, cache
from app.celery import scanner
from app.models import Users, Extensions
from app.utils import user_mgmt,tasks
from app.utils.scan import function,control

from urllib.parse import quote
from functools import wraps
from io import BytesIO
import datetime
import random
import time
import os
import zipfile

browser_bp = Blueprint("browser", __name__, template_folder="templates")

def check_scan(f):
	@wraps(f)
	def func(*args, **kwargs):
		if "scan" in session:
			if session["scan"] == True:
				return redirect(url_for("browser.scan_route"))
		else:
			session["scan"] = False
		return f(*args, **kwargs)
	return func

@browser_bp.before_request
@login_required
def before_request_browser_bp():
	if current_user.role != "User":
		logout_user()
		return redirect(url_for("login.login"))

def sizeof_fmt(num, suffix="B"):
	for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
		if abs(num) < 1024.0:
			return f"{num:3.1f} {unit}{suffix}"
		num /= 1024.0
	return f"{num:.1f} Yi{suffix}"

@browser_bp.route("/")
def index_browser():
	return redirect(url_for("browser.index"))

@browser_bp.route("/path/<path:MasterListDir>")
@browser_bp.route("/path/")
@check_scan
def index(MasterListDir=""):
	user = Users.query.filter_by(id=current_user.id).first()
	key_user = f"codeEP_{str(user.uuid)}"
	code_ep = cache.get(key_user)
	user_uuid = user.uuid
	joining = os.path.join(DATA_PATH,"data",str(user_uuid) ,MasterListDir)
	cur_dir = MasterListDir
	if not os.path.exists(joining):
		abort(404)
	if os.path.isdir(joining):
		new_path = os.listdir(joining)
		list_items = [i for i in os.walk(joining)][0]
		items_dir = []
		items_file = []
		for i in list_items[1]:
			j = os.path.join(joining, i)
			creation_date = str(
				datetime.datetime.fromtimestamp(os.lstat(j).st_ctime)
			).split(".")[0]
			modification_date = str(
				datetime.datetime.fromtimestamp(os.lstat(j).st_mtime)
			).split(".")[0]
			size = sizeof_fmt(os.lstat(j).st_size)
			iq = quote(i)
			# make [nom_fichier,date_de_creation,date_modifer,taille_fichier]
			make = [i, creation_date, modification_date, size, iq]
			items_dir.append(make)
		for i in list_items[2]:
			j = os.path.join(joining, i)
			creation_date = str(
				datetime.datetime.fromtimestamp(os.lstat(j).st_ctime)
			).split(".")[0]
			modification_date = str(
				datetime.datetime.fromtimestamp(os.lstat(j).st_mtime)
			).split(".")[0]
			size = sizeof_fmt(os.lstat(j).st_size)
			iq = quote(i)
			# make [nom_fichier,date_de_creation,date_modifer,taille_fichier]
			make = [i, creation_date, modification_date, size, iq]
			items_file.append(make)	
	return render_template(
		"browser.html", items_file=items_file, items_dir=items_dir, cur_dir=cur_dir, code=code_ep
	)


@browser_bp.route("/download/<path:MasterListDir>")
@browser_bp.route("/download/")
@check_scan
def download(MasterListDir=""):
	user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
	path = os.path.join(DATA_PATH,"data",str(user_uuid) ,MasterListDir)
	master_path = "/".join(path.split("/")[:-1])
	last = MasterListDir.split("/")[-1]
	name_in_file = last
	if last == "":
		last = "."
	if name_in_file == "":
		name_in_file="root"
	os.chdir(master_path)
	if os.path.exists(path):
		if os.path.isdir(path):
			timestr = time.strftime("%Y%m%d-%H%M%S")
			fileName = f"{name_in_file}_{timestr}.zip".format(timestr)
			memory_file = BytesIO()
			with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
				for root, dirs, files in os.walk(last):
					for file in files:
						zipf.write(os.path.join(root, file))
			memory_file.seek(0)
			return send_file(
				memory_file,
				as_attachment=True,
				mimetype="application/zip",
				download_name=fileName,
			)
		elif os.path.isfile(path):
			return send_file(path, as_attachment=True)
	else:
		return redirect(url_for("login.logout"))
	return ""


@browser_bp.route("/delete/<path:MasterListDir>")
@browser_bp.route("/delete/")
@check_scan
def delete(MasterListDir=""):
	user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
	path = os.path.join(DATA_PATH,"data",str(user_uuid) ,MasterListDir)
	master_path = "/".join(path.split("/")[:-1])
	last = MasterListDir.split("/")[-1]
	os.chdir(master_path)
	if os.path.exists(path):
		if os.path.isdir(path):
			for root, dirs, files in os.walk(last, topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
				for name in dirs:
					os.rmdir(os.path.join(root, name))
			os.rmdir(last)
			return "ok"
		elif os.path.isfile(path):
			os.remove(last) 
			return "ok"
	else:
		return redirect(url_for("login.logout"))
	return ""

@browser_bp.route("/scan",methods=["POST","GET"])
def scan_route():
	if request.method == "POST" and session["scan"] == False:
		session["scan_resultat"] = []
		try_start = False
		if request.files.getlist("fileInput")[0].filename == "" and request.files.getlist("folderInput")[0].filename == "":
			flash("Please upload file or folder")
			return redirect(url_for("browser.index"))
		session["scan"] = True
		user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
		path = os.path.join(DATA_PATH,"scan",str(user_uuid))
		req = request.files
		# query extension
		query_extension = Extensions.query.filter_by(valid=True).all()
		valid_extension = [ext.mimetype for ext in query_extension]

		# File saving
		req_file = request.files.getlist("fileInput")
		for file in req_file:
			file_reader = file.read()
			file_name = file.filename
			file_length = len(file_reader)
			if file_name != "" or file_length != 0:
				filename = secure_filename(file_name)
				file_path = os.path.join(path, filename)
				if control.control(file_reader,valid_extension):
					open(file_path,"wb").write(file_reader)
					try_start = True
				else:
					to_append = f"The file '{str(filename)}' has not an authorized extension and it can't be scan"
					log.info(to_append)
					session["scan_resultat"].append(str(to_append))

		# Folder saving
		req_folder = req.getlist("folderInput")
		for file in req_folder:
			file_reader = file.read()
			if file.filename != "" or len(file_reader) != 0:
				file_name = file.filename
				file_mime = file.mimetype
				file_length = len(file_reader)
				split_in_folder = file.filename.split("/")
				if len(split_in_folder) > 15 or "" in split_in_folder or ".." in split_in_folder or "%" in split_in_folder:
					flash("bad upload folder")
					session["scan"] = False
					return redirect(url_for("browser.path"))
				folder_creation = "/".join(i for i in split_in_folder[:-1])
				if not os.path.exists(os.path.join(path,folder_creation)):
					os.makedirs(os.path.join(path,folder_creation))
				filename = secure_filename(file_name)
				if control.control(file_reader,valid_extension):
					file_path = os.path.join(path,folder_creation,filename)
					open(file_path,"wb").write(file_reader)
					try_start = True
				else:
					session["scan_resultat"].append(f"The file '{str(filename)}' has not an authorized extension and it can't be scan")
		# Start scan
		if try_start:
			scan_id = function.start_scan()
			session["scan_id"] = scan_id
		else:
			session["scan"] = False
			return redirect(url_for("browser.index"))
	elif request.method == "GET" and session["scan"] == False:
		return redirect(url_for("browser.index"))
	return render_template("scan.html",scan_id=str(session["scan_id"]))

@browser_bp.route("/scan/id/<string:id>")
def scan_id(id=""):
	id = str(id)
	res = scanner.GroupResult.restore(id)
	# log.info(str(res.get()))
	# log.info(res.ready())
	if res.ready():
		function.parse_result()
		function.end_scan(id)
		flash("Scan ended")
		session["scan"] = False 
	return {"state":res.ready()}

@browser_bp.route("/code",methods=["POST"])
@check_scan
def code():
	user = Users.query.filter_by(id=current_user.id).first()
	key_user = f"codeEP_{str(user.uuid)}"
	if cache.get(key_user) is None:
		cache.set(key_user,user_mgmt.get_code(),timeout=1800)
	return redirect(request.referrer)

@browser_bp.route("/temp_scan_off")
def temp():
	session["scan"] = False 
	return redirect(url_for("browser.index"))