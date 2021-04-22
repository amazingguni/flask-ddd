
import pytest

from app.catalog.domain.product import Product
from app.user.domain.user import User
from app.cart.domain.cart import Cart

from app.order.domain.order_state import OrderState
from app.order.application.place_order_service import PlaceOrderService


@pytest.fixture(scope='function')
def place_order_service(cart_repository, order_repository):
    return PlaceOrderService(
        cart_repository=cart_repository, order_repository=order_repository)


def test_place_order(pre_data_db_session, place_order_service, shipping_info):
    # Given
    product = pre_data_db_session.query(Product).first()
    orderer = pre_data_db_session.query(User).first()
    cart = Cart(product=product, user=orderer, quantity=1)
    pre_data_db_session.add(cart)

    # When
    order = place_order_service.place_order(orderer, shipping_info)

    # Then
    assert order.orderer == orderer
    assert order.shipping_info.receiver.phone == shipping_info.receiver.phone
    assert order.shipping_info.receiver.name == shipping_info.receiver.name
    assert order.state == OrderState.PAYMENT_WAITING
    assert len(order.order_lines) == 1
