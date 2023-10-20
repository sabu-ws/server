from flask import Blueprint

browser_bp = Blueprint(
	"browser",
	__name__,
	template_folder="templates"
	)

@browser_bp.route("/")
def index():
	return "comming soon"