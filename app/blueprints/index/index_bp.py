from flask import Blueprint,render_template, request, url_for, redirect, flash
from app import db
from app.models import Setup, Users
from app.forms import LoginForm
# , NetworkSettingsForm
from app.utils import logging

from config import *

import re
import json
import os


index_bp = Blueprint(
	"index",
	__name__,
	template_folder="templates"
	# static_folder="../../../static"
	)


@index_bp.route("/",methods=["GET"])
def index():
	return redirect("/login")


# @index_bp.route("/setup",methods=["POST","GET"])
# def setup():
# 	setup_db = Setup()
# 	init_db = setup_db.query.all()
# 	if len(init_db) == 0:
# 		globalsetup = Setup(action="global",state=False)
# 		password = Setup(action="password",state=False)
# 		network = Setup(action="network",state=False)
# 		db.session.add(globalsetup)
# 		db.session.add(password)
# 		db.session.add(network)
# 		db.session.commit()

# 	networkform = NetworkSettingsForm()
# 	passwordform = LoginForm()
# 	if request.method=="GET":
# 		get_all_state = setup_db.query.filter_by(state=True).all()
# 		if len(get_all_state)>0:
# 			flash("The installation was start. Please wait the reboot...")
# 	if request.method=="POST":
# 		get_all_state = setup_db.query.filter_by(state=True).all()
# 		if len(get_all_state)>0:
# 			redirect(url_for("index.setup"))

# 		if networkform.interface.validate(networkform) and networkform.ipaddr.validate(networkform) and networkform.netmask.validate(networkform) and networkform.gateway.validate(networkform) and networkform.dns1.validate(networkform):
# 			if not networkform.dns2.validate(networkform):
# 				if networkform.dns2.data == "":
# 					networkform.dns2.data = "9.9.9.9"
# 			if passwordform.password.validate(passwordform):
# 				interface = networkform.interface.data
# 				ip = networkform.ipaddr.data
# 				netmask = networkform.netmask.data
# 				gateway = networkform.gateway.data
# 				dns1 = networkform.dns1.data
# 				dns2 = networkform.dns2.data
# 				mdp = passwordform.password.data

# 				dico_network = {"interface": interface, "ip": ip, "netmask": netmask, "gateway": gateway, "dns1": dns1, "dns2": dns2}
# 				dico_category_network = {"network": dico_network}
# 				json_config = open(CONFIG_PATH+"/config.json", "w")
# 				json.dump(dico_category_network, json_config)
# 				os.popen(f"{SCRIPT_PATH}/network/network-config.sh")
# 				getNetworkStatus = setup_db.query.filter_by(action="network").first()
# 				getNetworkStatus.state = True
# 				db.session.commit()

# 				set_admin_user = User(username="admin")
# 				set_admin_user.set_password(mdp)
# 				db.session.add(set_admin_user)
# 				getPasswordStatus = setup_db.query.filter_by(action="password").first()
# 				getPasswordStatus.state = True
# 				db.session.commit()

# 				logging("setup","The informations was setup")

# 				os.popen("sleep 3 && sudo bash /sabu/config/install.sh")
# 				return redirect(url_for("index.setup"))
# 			else:
# 				flash("The password was incorrect!")
# 				return redirect(url_for("index.setup"))
# 		else:
# 			flash("Some informations of network was incorrect!")
# 			return redirect(url_for("index.setup"))
# 	else:
# 		redirect("/404")

# 		return render_template("setup.html",networkform=networkform,passwordform=passwordform)
