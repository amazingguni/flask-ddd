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

    @app.route('/')
    # pylint: disable=unused-variable
    def home():
        return render_template('home.html')

    from .user import views as user_views
    from .catalog import views as catalog_views
    from .admin import views as admin_views

    views = [user_views, catalog_views, admin_views]
    register_blueprints(app, views)

    from .containers import Container
    container = Container(app=app, session=db.session)
    app.container = container
    with app.app_context():
        container.wire(modules=views)

    return app


def register_blueprints(app, views):
    for view in views:
        app.register_blueprint(view.bp)


@login_manager.user_loader
def load_user(user_id):
    from .user.domain.user import User
    return User.query.filter(User.id == user_id).first()
