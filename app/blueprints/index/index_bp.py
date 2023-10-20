from flask import Blueprint, redirect

from config import *


index_bp = Blueprint(
	"index",
	__name__,
	template_folder="templates"
	)


@index_bp.route("/",methods=["GET"])
def index():
	return redirect("/login")