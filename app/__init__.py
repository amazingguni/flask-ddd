import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_name)
    CORS(app)

    db.init_app(app)

    return app






