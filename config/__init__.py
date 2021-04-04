import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///db.sqlite')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
