from contextlib import contextmanager
import os

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate(db=db)


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(
        os.environ.get('APP_SETTINGS', 'config.development.DevelopmentConfig'))
    CORS(app)

    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    from .user.domain.user import User

    @login_manager.user_loader
    # pylint: disable=unused-variable
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    @app.route('/')
    # pylint: disable=unused-variable
    def home():
        return render_template('home.html')

    # Blueprints
    from .user.views import bp as user_bp
    app.register_blueprint(user_bp)
    from .catalog.views import bp as catalog_bp
    app.register_blueprint(catalog_bp)
    from .admin import views as admin_views
    app.register_blueprint(admin_views.bp)

    from .containers import Container
    container = Container(app=app, session=db.session)
    container.wire(modules=[admin_views])

    return app
