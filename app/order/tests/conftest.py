import pytest

from app.order.domain.order import Order

@pytest.fixture(scope='function')
def order(db_session):
    _order = Order()
    db_session.add(_order)
    db_session.commit()
    return _order    
