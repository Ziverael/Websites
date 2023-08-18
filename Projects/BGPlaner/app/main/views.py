from flask import render_template, request, url_for, flash, session
from . import main
from ..db import get_db
from flask_login import login_user, current_user, login_required, logout_user

@main.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")
