from app.order.domain.order import Order
from app.order.domain.order_state import OrderState
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address

from app.order.infra.repository.sql_order_repository import SqlOrderRepository


def test_save(db_session, loginned_user, shipping_info):
    # Given
    order = Order(
        orderer=loginned_user,
        shipping_info=shipping_info,
        state=OrderState.PAYMENT_WAITING
    )

    # When
    SqlOrderRepository(db_session).save(order)

    # Then
    assert db_session.query(Order).count() == 1


def test_find_all(pre_data_db_session):
    # When
    orders = SqlOrderRepository(pre_data_db_session).find_all()

    # Then
    assert len(orders) == 4


def test_find_by_id(pre_data_db_session, order):
    # When
    return_order = SqlOrderRepository(pre_data_db_session).find_by_id(order.id)

    # Then
    assert return_order.id == order.id
