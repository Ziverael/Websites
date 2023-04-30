import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask import Blueprint

from .config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name = "default"):
    """Function factory"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # print(app.config["SQLALCHEMY_DATABASE_URI"])
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


    #Rewrite on blueprints

    # @app.route('/rank/<genre>')
    # def rank_genre(genre):
    #     pass

    # @app.route('/rank/<genre>/<game>')
    # def rank_game(game):
    #     #From game you can get genre value
    #     pass

    from .main import main as main_bp
    app.register_blueprint(main_bp)


    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix = "/auth")




    
    # from .genreTop import genreTop as genTop_bp
    # app.register_blueprint(genTop_bp, url_prefix = '/genreTop')
    
    
    return app    
