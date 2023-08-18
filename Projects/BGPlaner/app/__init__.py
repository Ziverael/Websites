import os
from flask import Flask, render_template, Blueprint
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from .config import config

mail = Mail()
login = LoginManager()

def create_app(config_name : str = "default", config_ini = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
 
    #If ini file passed then update fields in config file
    if config_ini:
        for cfg_key in config_ini[config_name]:
            app.config[cfg_key.upper()] = config_ini[config_name][cfg_key]
    config[config_name].init_app(app)


    from .  import db
    db.init_app(app)
    mail.init_app(app)
    login.init_app(app)


    from .auth import  auth as bp_auth
    app.register_blueprint(bp_auth, url_prefix = "/auth")

    from .main import main as bp_main
    app.register_blueprint(bp_main, url_prefix = "/")


    #Login manager customization
    login.session_protection = "strong"
    login.login_view = "auth.login"
    login.login_message = "Login to enter this page."

    return app