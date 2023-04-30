import os
import configparser
from app import create_app
from app.db import Connection
import click

config = configparser.ConfigParser()
config.read(".env.ini")
app = create_app(config["local"]["mode"] or 'default')




@app.shell_context_processor
def make_shell_context():
    return dict(
        app = app
        )

# @app.cli.command()
# @click.option("--coverage/--no-coverage", default = False, help = "Enable code coverage")
# def test(coverage):
#     """Run the unit test."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests') # It find test and read file. If there is executable fragments that line would execute it
#     unittest.TextTestRunner(verbosity = 2).run(tests) # It run TestCases
    
