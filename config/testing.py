import os
from . import Config


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///test.db.sqlite')

    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL', 'sqlite:///:memory:')
