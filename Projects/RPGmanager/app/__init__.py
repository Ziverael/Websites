import os
from flask import Flask, render_template, Blueprint
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from .config import config

mail = Mail()
login = LoginManager()
login.session_protection = "strong"

def create_app(config_name : str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .  import db
    db.init_app(app)
    mail.init_app(app)
    login.init_app(app)


    from .auth import  auth as bp_auth
    app.register_blueprint(bp_auth, url_prefix = "/auth")
    return app