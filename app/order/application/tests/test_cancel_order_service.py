import pytest
from unittest import mock
from app.order.domain.order_state import OrderState
from ..cancel_order_service import CancelOrderService


@pytest.fixture(scope='function')
def cancel_order_service(order_repository):
    return CancelOrderService(order_repository)


@mock.patch('app.order.application.cancel_order_service.RefundHandler.handle')
def test_cancel(mock_handle, db_session, cancel_order_service, loginned_user, order):
    # When
    cancel_order_service.cancel(order.id, loginned_user)

    # Then
    db_session.refresh(order)
    assert order.state == OrderState.CANCELED
    mock_handle.assert_called_with(mock.ANY)
