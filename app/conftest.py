import pytest

from app import create_app
from app import db as _db

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
def db(app, request):
    """ Session-wide test database """
    _db.drop_all()
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()



@pytest.fixture(scope='function')
def session(db, request):
    """ Creates a new database session for a test """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()