import pytest
import sqlalchemy as sa

from app import create_app
from app import db
from app.user.domain.user import User
from datetime import datetime

from app.catalog.domain.category import Category
from app.catalog.domain.product import Product
from app.order.domain.order import Order
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address
from app.order.domain.order_state import OrderState
from app.order.domain.order_line import OrderLine

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


@pytest.fixture(scope='function')
def _db(app):
    """ Session-wide test database """
    db.drop_all()
    db.app = app
    db.create_all()

    yield db

    db.drop_all()

@pytest.fixture(scope='function')
def _transaction(request, _db):
    '''
    Create a transactional context for tests to run in.
    '''
    # Start a transaction
    connection = _db.engine.connect()
    transaction = connection.begin()

    # Bind a session to the transaction. The empty `binds` dict is necessary
    # when specifying a `bind` option, or else Flask-SQLAlchemy won't scope
    # the connection properly
    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    # Begin a nested transaction (any new transactions created in the codebase
    # will be held until this outer transaction is committed or closed)
    session.begin_nested()

    # Each time the SAVEPOINT for the nested transaction ends, reopen it
    @sa.event.listens_for(session, 'after_transaction_end')
    def restart_savepoint(session, trans):
        if trans.nested and not trans._parent.nested:
            # ensure that state is expired the way
            # session.commit() at the top level normally does
            session.expire_all()
            session.begin_nested()

    # Force the connection to use nested transactions
    connection.begin = connection.begin_nested

    # If an object gets moved to the 'detached' state by a call to flush the session,
    # add it back into the session (this allows us to see changes made to objects
    # in the context of a test, even when the change was made elsewhere in
    # the codebase)
    @sa.event.listens_for(session, 'persistent_to_detached')
    @sa.event.listens_for(session, 'deleted_to_detached')
    def rehydrate_object(session, obj):
        session.add(obj)

    @request.addfinalizer
    def teardown_transaction():
        # Delete the session
        session.remove()

        # Rollback the transaction and return the connection to the pool
        transaction.rollback()
        connection.close()

    return connection, transaction, session


@pytest.fixture(scope='function')
def _session(pytestconfig, _transaction):
    _, _, session = _transaction
    return session


@pytest.fixture(scope='function')
def db_session(_session, _transaction):
    return _session



@pytest.fixture(scope='function')
def pre_data_db_session(db_session):
    user1 = User(username='사용자1', password='1234', blocked=False, is_admin=False)
    user2 = User(username='사용자2', password='5678', blocked=False, is_admin=False)
    admin = User(username='운영자', password='5678', blocked=False, is_admin=True)
    '''
    TODO: add permission
    insert into member_authorities values ('user1', 'ROLE_USER');
    insert into member_authorities values ('user2', 'ROLE_USER');
    insert into member_authorities values ('admin', 'ROLE_ADMIN');
    ''' 
    db_session.add_all([user1, user2, admin])

    category1 = Category(name='전자제품')
    category2 = Category(name='필기구')
    db_session.add_all([category1, category2])

    product1 = Product(
        name='라즈베리파이3 모델B', price = 56000, detail='모델B')
    product1.categories.append(category1)
    '''
    TODO: add image to product1
    insert into image (product_id, list_idx, image_type, image_path, upload_time) values
    ('prod-001', 0, 'II', 'rpi3.jpg', now());
    insert into image (product_id, list_idx, image_type, image_path, upload_time) values
    ('prod-001', 1, 'EI', 'http://external/image/path', now());
    '''
    product2 = Product(
        name='어프로치 휴대용 화이트보드 세트', price = 11920, detail='화이트보드')
    product2.categories.append(category2)
    '''
    TODO: add image to product2
    insert into image (product_id, list_idx, image_type, image_path, upload_time) values
    ('prod-002', 0, 'II', 'wbp.png', now());
    '''
    product3 = Product(
        name='볼펜 겸용 터치펜', price = 9000, detail='볼펜과 터치펜을 하나로!')
    product3.categories.append(category1)
    product3.categories.append(category2)
    '''
    TODO: add image to product3
    insert into image (product_id, list_idx, image_type, image_path, upload_time) values
    ('prod-003', 0, 'II', 'pen.jpg', now());
    insert into image (product_id, list_idx, image_type, image_path, upload_time) values
    ('prod-003', 1, 'II', 'pen2.jpg', now());
    '''
    db_session.add_all([product1, product2, product3])
    
    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order1 = Order(
        orderer=user1, shipping_info=shipping_info, 
        total_amounts=4000, state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-01 15:30:00')
        )
    order1.order_lines.append(
        OrderLine(product=product1, price=1000, quantity=2, amounts=2000))
    order1.order_lines.append(
        OrderLine(product=product2, price=2000, quantity=1, amounts=2000))
    
    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order2 = Order(
        orderer=user1, shipping_info=shipping_info, 
        total_amounts=5000, state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-02 09:18:21')
        )
    order2.order_lines.append(
        OrderLine(product=product1, price=1000, quantity=5, amounts=5000))

    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order3 = Order(
        orderer=user2, shipping_info=shipping_info, 
        total_amounts=5000, state=OrderState.SHIPPED,
        order_date=datetime.fromisoformat('2016-01-03 09:00:00')
        )
    order3.order_lines.append(
        OrderLine(product=product1, price=1000, quantity=5, amounts=5000))

    db_session.add_all([order1, order2, order3])
    '''
    insert into article (title) values ('제목');
    insert into article_content values (1, 'content', 'type');

    insert into evententry (type, content_type, payload, timestamp) values
    ('com.myshop.eventstore.infra.SampleEvent', 'application/json', '{"name": "name1", "value": 11}', now());
    insert into evententry (type, content_type, payload, timestamp) values
    ('com.myshop.eventstore.infra.SampleEvent', 'application/json', '{"name": "name2", "value": 12}', now());
    insert into evententry (type, content_type, payload, timestamp) values
    ('com.myshop.eventstore.infra.SampleEvent', 'application/json', '{"name": "name3", "value": 13}', now());
    insert into evententry (type, content_type, payload, timestamp) values
    ('com.myshop.eventstore.infra.SampleEvent', 'application/json', '{"name": "name4", "value": 14}', now());
    '''
    return db_session