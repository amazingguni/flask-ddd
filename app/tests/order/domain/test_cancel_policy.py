from app.user.domain.user import User
from app.order.domain.cancel_policy import CancelPolicy


def test_has_cancellation_permission_GIVEN_owner_THEN_True(loginned_user, order):
    assert CancelPolicy().has_cancellation_permission(order, loginned_user) == True


def test_has_cancellation_permission_GIVEN_not_owner_THEN_False(db_session, order):
    other_user = User(username='other_user', password='1234',
                      blocked=False, is_admin=False)
    db_session.add(other_user)
    assert CancelPolicy().has_cancellation_permission(order, other_user) == False


def test_has_cancellation_permission_GIVEN_admin_THEN_True(db_session, order):
    admin_user = User(username='admin_user', password='1234',
                      blocked=False, is_admin=True)
    db_session.add(admin_user)
    assert CancelPolicy().has_cancellation_permission(order, admin_user) == True
