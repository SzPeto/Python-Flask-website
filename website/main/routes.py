from flask import Blueprint, render_template
from flask_login import current_user

from website.main.utils import *

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html", title = "Home", current_user=current_user)