import pytest
from unittest import mock
from app.order.domain.order_state import OrderState
from app.order.domain.exceptions import AlreadyShippedException
from app.order.infra.paygate.external_refund_service import ExternalRefundService
from app.order.application.cancel_order_service import CancelOrderService


@pytest.fixture(scope='function')
def cancel_order_service(order_repository):
    return CancelOrderService(order_repository, ExternalRefundService())


@mock.patch('app.order.application.cancel_order_service.RefundHandler.handle')
def test_cancel(mock_handle, db_session, cancel_order_service, loginned_user, order):
    # When
    cancel_order_service.cancel(order.id, loginned_user)

    # Then
    db_session.refresh(order)
    assert order.state == OrderState.CANCELED
    mock_handle.assert_called_with(mock.ANY)


def test_cancel_GIVEN_AFTER_SHIPPED_THEN_ERROR(db_session, cancel_order_service, loginned_user, order):
    # Given
    after_shipped_state = [OrderState.SHIPPED,
                           OrderState.DELIVERING, OrderState.DELIVERY_COMPLETED]

    # When
    for state in after_shipped_state:
        order.state = state
        db_session.add(order)
        with pytest.raises(AlreadyShippedException):
            cancel_order_service.cancel(order.id, loginned_user)
