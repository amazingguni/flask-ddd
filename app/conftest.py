import pytest

from app import create_app
from app import db

@pytest.fixture(scope='session')
def app(request):
    """ Session wide test 'Flask' application """
    app = create_app('config.testing.TestingConfig')
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def _db(app):
    """ Session-wide test database """
    db.drop_all()
    db.app = app
    db.create_all()

    yield db

    db.drop_all()
