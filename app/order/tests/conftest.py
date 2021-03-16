import pytest

from app.order.domain.order import Order

@pytest.fixture(scope='function')
def order(session):
    _order = Order()
    session.add(_order)
    session.commit()
    return _order    
