#!/usr/bin/env python3
#This code no longer works with new Flask release. Expected migration to flask CLI with flasky.py script
import os

# from GameScore.auth
from GameScore import create_app, db
from GameScore.models import User, Game,  Review
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv("FLASK_CONFIG") or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app = app,
        db = db,
        User = User,
        Review = Review,
        Game = Game
    )

manager.add_command("shell", Shell(make_context = make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()