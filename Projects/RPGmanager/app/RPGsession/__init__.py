from flask import Blueprint

rpgSession = Blueprint("RPGsession", __name__)

from . import views