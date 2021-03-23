import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(
        os.environ.get('APP_SETTINGS', 'config.development.DevelopmentConfig'))
    CORS(app)

    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    # Blueprints
    from app.catalog.ui import blueprint as catalog_blueprint
    app.register_blueprint(catalog_blueprint)

    

    return app






