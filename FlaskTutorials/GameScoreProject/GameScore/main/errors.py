from flask import render_template
from . import main

#app_errorhandler is equvalent of errorhandler but for a blueprint
@main.app_errorhandler(404)
def page_not_found(e):
    err_string = str(e)
    return render_template('error.html', value = err_string), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    err_string = str(e)
    return render_template('error.html', value = err_string), 500
