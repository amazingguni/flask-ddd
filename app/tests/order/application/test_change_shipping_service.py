import pytest
from app.order.application.change_shipping_service import ChangeShippingService
from app.order.application.exceptions import NoOrderException


@pytest.fixture(scope='function')
def change_shipping_service(order_repository):
    return ChangeShippingService(order_repository)


def test_change(db_session, change_shipping_service, order, shipping_info):
    shipping_info.receiver.name = 'Changed receiver'
    shipping_info.address.address1 = 'changed address1'
    shipping_info.address.address2 = 'changed address2'

    # When
    change_shipping_service.change(order.id, shipping_info)

    # Then
    db_session.refresh(order)
    assert order.shipping_info.receiver.name == 'Changed receiver'
    assert order.shipping_info.address.address1 == 'changed address1'
    assert order.shipping_info.address.address2 == 'changed address2'


def test_change_GIVEN_invalid_order_THEN_error(db_session, change_shipping_service, order, shipping_info):
    shipping_info.receiver.name = 'Changed receiver'
    invalid_order_id = 100

    # When
    with pytest.raises(NoOrderException):
        change_shipping_service.change(invalid_order_id, shipping_info)
