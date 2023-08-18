from flask import render_template, redirect, request, url_for, flash, session
# from ..login import 
from ..db import get_db
from . import rpgSession
from flask_login import current_user, login_required


@rpgSession.route('/lobby', methods = ["GET", "POST"])
def lobby():
    return render_template("lobby.html")