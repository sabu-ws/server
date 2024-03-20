from config import *
from flask import Blueprint, redirect, url_for, render_template, abort, session, send_file, request
from werkzeug.utils import secure_filename

from app import login_required, current_user, logout_user, logger as log
from app.models import Users
from app.utils import scan

from urllib.parse import quote
from io import BytesIO
import datetime
import time
import os
import zipfile

browser_bp = Blueprint("browser", __name__, template_folder="templates")


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


@browser_bp.route("/path/<path:MasterListDir>")
@browser_bp.route("/path/")
def index(MasterListDir=""):
	user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
	joining = os.path.join(DATA_PATH,"data",str(user_uuid) ,MasterListDir)
	cur_dir = MasterListDir + "/" if MasterListDir != "" else ""
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
		"browser.html", items_file=items_file, items_dir=items_dir, cur_dir=cur_dir
	)


@browser_bp.route("/download/<path:MasterListDir>")
@browser_bp.route("/download/")
def download(MasterListDir=""):
	user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
	path = os.path.join(DATA_PATH,"data",str(user_uuid) ,MasterListDir)
	master_path = "/".join(path.split("/")[:-1])
	last = MasterListDir.split("/")[-1]
	os.chdir(master_path)
	if os.path.exists(path):
		if os.path.isdir(path):
			timestr = time.strftime("%Y%m%d-%H%M%S")
			fileName = f"{last}_{timestr}.zip".format(timestr)
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

@browser_bp.route("/scan",methods=["POST"])
def scan():
	user_uuid = Users.query.filter_by(id=current_user.id).first().uuid
	path = os.path.join(DATA_PATH,"scan",str(user_uuid))
	req = request.files
	# File saving
	req_file = req.getlist("files[]")
	for i in req_file:
		file_name = i.filename
		file = i
		file_length = len(i.read())
		if file and file_name != "" and file_length != 0:
			filename = secure_filename(file.filename)
			file.save(os.path.join(path, filename))
	# Folder saving
	req_folder = req.getlist("folder[]")
	for file in req_folder:
		split_in_folder = file.filename.split("/")
		if len(split_in_folder) > 15 or "" in split_in_folder or ".." in split_in_folder or "%" in split_in_folder:
			flash("bad upload folder")
			return redirect(url_for("browser.path"))
		folder_creation = "/".join(i for i in split_in_folder[:-1])
		if not os.path.exists(os.path.join(path,folder_creation)):
			os.makedirs(os.path.join(path,folder_creation))
		filename = secure_filename(file.filename)
		file.save(os.path.join(path,folder_creation,filename))
	return render_template("scan.html")