import pytest
from app.order.domain.order_state import OrderState
from ..cancel_order_service import CancelOrderService


@pytest.fixture(scope='function')
def cancel_order_service(order_repository):
    return CancelOrderService(order_repository)


def test_cancel(db_session, cancel_order_service, loginned_user, order):
    # When
    cancel_order_service.cancel(order.id, loginned_user)

    # Then
    db_session.refresh(order)
    assert order.state == OrderState.CANCELED
