"""
To run Flasky project:

export FLASK_APP=flasky.py
flask run


To upgrade Flasky database to last version, just run
$flask db upgrade

Featured with unit test is under constraction.
"""

import os
from GameScore import create_app, db
from GameScore.models import User, Game, Review
from flask_migrate import Migrate
import click

app = create_app(os.getenv("FLASK_CONFIG") or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        app = app,
        db=db,
        User = User,
        Review = Review,
        Game = Game
        )

@app.cli.command()
@click.option("--coverage/--no-coverage", default = False, help = "Enable code coverage")
def test(coverage):
    """Run the unit test."""
    import unittest
    tests = unittest.TestLoader().discover('tests') # It find test and read file. If there is executable fragments that line would execute it
    unittest.TextTestRunner(verbosity = 2).run(tests) # It run TestCases
    
