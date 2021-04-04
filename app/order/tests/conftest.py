import pytest
from app.user.domain.user import User
from app.order.domain.order import Order
from app.order.infra.dao.sql_order_summary_dao import SqlOrderSummaryDao


@pytest.fixture(scope='function')
def orderer(db_session):
    _orderer = User(username='사용자', password='1234',
                    blocked=False, is_admin=False)
    db_session.add(_orderer)
    db_session.commit()
    return _orderer


@pytest.fixture(scope='function')
def order(db_session, orderer):
    _order = Order(orderer=orderer)
    db_session.add(_order)
    db_session.commit()
    return _order


@pytest.fixture(scope='function')
def sql_order_summary_dao(pre_data_db_session):
    return SqlOrderSummaryDao(pre_data_db_session)
