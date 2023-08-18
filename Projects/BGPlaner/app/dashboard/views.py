from flask import render_template, request, url_for, flash, session
from . import dashboard
from ..db import get_db


#Only for admin: create form
@dashboard.route('/dashboard', methods = ["GET", "POST"])
def create_form():

#For all: vote (user can vote once)
