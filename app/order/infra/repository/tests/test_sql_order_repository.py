from app.order.domain.order import Order
from app.order.domain.order_state import OrderState
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address

from ..sql_order_repository import SqlOrderRepository


def test_save(db_session, loginned_user, shipping_info):
    # Given
    order = Order(
        orderer=loginned_user,
        shipping_info=shipping_info,
        total_amounts=10000,
        state=OrderState.PAYMENT_WAITING
    )

    # When
    SqlOrderRepository(db_session).save(order)

    # Then
    assert db_session.query(Order).count() == 1
