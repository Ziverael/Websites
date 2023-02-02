from datetime import datetime
from flask import render_template, session, url_for, redirect
from . import main

@main.route('/', methods = [ "GET", "POST"])
def index():
    return render_template("index.html", 
    name = session.get("name"),
    known = session.get("known", False),
    current_time = datetime.utcnow()), 200