#!/usr/bin/env python
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import create_app, db

app = create_app(
    os.getenv('APP_SETTINGS', 'config.development.DevelopmentConfig'))
manager = Manager(app)
migrate = Migrate(app, db)


# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)


# manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0"))


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
