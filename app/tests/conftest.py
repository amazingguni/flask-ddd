from flask import template_rendered
from datetime import datetime
import pytest

from app import create_app
from app import db as app_db
from app.user.domain.user import User

from app.catalog.domain.category import Category
from app.catalog.domain.product import Product
from app.order.domain.order import Order
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address
from app.order.domain.order_state import OrderState
from app.order.domain.order_line import OrderLine


@pytest.fixture(scope='session')
def app():
    """ Session wide test 'Flask' application """
    _app = create_app('config.testing.TestingConfig')
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    yield app.test_client()
    ctx.pop()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(scope='function')
def db(app):
    _db = app_db
    _db.drop_all()
    _db.create_all()
    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def db_session(db):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.session

    yield db.session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def loginned_user(app, db_session):
    user = User(username='loginned_user', password='1234',
                blocked=False, is_admin=False)
    db_session.add(user)
    db_session.commit()

    @app.login_manager.request_loader
    def load_user_from_request(request):
        return user
    return user


@pytest.fixture(scope='function')
def category(db_session):
    _category = Category(name='과자류')
    db_session.add(_category)
    return _category


@pytest.fixture(scope='function')
def product(db_session, category):
    _product = Product(
        name='꼬북칩', price=1000, detail='맛있는 꼬북칩')
    _product.categories.append(category)
    db_session.add(_product)
    db_session.flush()
    return _product


@pytest.fixture(scope='function')
def order(db_session, loginned_user, shipping_info, product):
    _order = Order(orderer=loginned_user,
                   shipping_info=shipping_info, state=OrderState.PREPARING)
    order_line = OrderLine(order=_order, product=product, quantity=1)
    _order.order_lines.append(order_line)
    db_session.add(_order)
    db_session.flush()
    return _order


@pytest.fixture(scope='function')
def shipping_info():
    receiver = Receiver(name='guni', phone='010-0000-0000')
    address = Address(zip_code='00000', address1='seoul', address2='seocho-gu')
    shipping_info = ShippingInfo(
        receiver=receiver, address=address, message='Fast please')
    return shipping_info


@pytest.fixture(scope='function')
def pre_data_db_session(db_session, order):
    user1 = User(username='사용자1', password='1234',
                 blocked=False, is_admin=False)
    user2 = User(username='사용자2', password='5678',
                 blocked=False, is_admin=False)
    admin = User(username='운영자', password='5678', blocked=False, is_admin=True)
    # TODO: add permission
    # insert into member_authorities values ('user1', 'ROLE_USER');
    # insert into member_authorities values ('user2', 'ROLE_USER');
    # insert into member_authorities values ('admin', 'ROLE_ADMIN');
    db_session.add_all([user1, user2, admin])

    category1 = Category(name='전자제품')
    category2 = Category(name='필기구')
    db_session.add_all([category1, category2])

    product1 = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')
    product1.categories.append(category1)
    product2 = Product(
        name='어프로치 휴대용 화이트보드 세트', price=11920, detail='화이트보드')
    product2.categories.append(category2)
    product3 = Product(
        name='볼펜 겸용 터치펜', price=9000, detail='볼펜과 터치펜을 하나로!')
    product3.categories.append(category1)
    product3.categories.append(category2)
    db_session.add_all([product1, product2, product3])

    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order1 = Order(
        orderer=user1, shipping_info=shipping_info,
        state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-01 15:30:00')
    )
    order1.order_lines.append(
        OrderLine(product=product1, quantity=2))
    order1.order_lines.append(
        OrderLine(product=product2, quantity=1))

    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order2 = Order(
        orderer=user1, shipping_info=shipping_info,
        state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-02 09:18:21')
    )
    order2.order_lines.append(
        OrderLine(product=product1, quantity=5))

    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    order3 = Order(
        orderer=user2, shipping_info=shipping_info,
        state=OrderState.SHIPPED,
        order_date=datetime.fromisoformat('2016-01-03 09:00:00')
    )
    order3.order_lines.append(
        OrderLine(product=product1, quantity=5))

    db_session.add_all([order1, order2, order3])
    return db_session


@pytest.fixture(scope='function')
def order_summary_dao(db_session):
    from app.order.infra.dao.sql_order_summary_dao import SqlOrderSummaryDao
    return SqlOrderSummaryDao(db_session)


@pytest.fixture(scope='function')
def category_repository(db_session):
    from app.catalog.infra.repository.sql_category_repository import SqlCategoryRepository
    return SqlCategoryRepository(db_session)


@pytest.fixture(scope='function')
def product_repository(db_session):
    from app.catalog.infra.repository.sql_product_repository import SqlProductRepository
    return SqlProductRepository(db_session)


@pytest.fixture(scope='function')
def cart_repository(db_session):
    from app.cart.infra.repository.sql_cart_repository import SqlCartRepository
    return SqlCartRepository(db_session)


@pytest.fixture(scope='function')
def order_repository(db_session):
    from app.order.infra.repository.sql_order_repository import SqlOrderRepository
    return SqlOrderRepository(db_session)
