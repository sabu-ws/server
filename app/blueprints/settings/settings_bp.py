from flask import Blueprint, render_template, redirect, url_for, request, flash

from app import login_required, current_user, bcrypt

from app.utils import logging
# from app.forms import LoginForm
from app.models import User
from config import *

settings_bp = Blueprint(
	"settings",
	__name__,
	template_folder="templates"
	)

@settings_bp.route("/",methods=["GET","POST"])
@login_required()
def settings():
	return "settings page"
	return render_template("settings.html")