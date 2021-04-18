from flask import url_for
from app.user.domain.user import User


def test_order_detail(db_session, client, captured_templates, loginned_user, order):
    # When
    response = client.get(
        url_for('user.order_detail', order_id=order.id))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'user/order_detail.html.j2'
    assert context['order'].id == order.id


def test_order_detail_GIVEN_no_order_THEN_no_order_page(client, captured_templates, loginned_user):
    invalid_order_id = 100

    # When
    response = client.get(
        url_for('user.order_detail', order_id=invalid_order_id))

    # Then
    assert response.status_code == 200
    template, _ = captured_templates[0]
    assert template.name == 'user/no_order.html.j2'


def test_order_detail_GIVEN_others_order_THEN_not_your_order_page(
        app, db_session, client, captured_templates, loginned_user, order):
    # Given
    other_user = User(username='other_user', password='1234',
                      blocked=False, is_admin=False)
    db_session.add(other_user)

    @app.login_manager.request_loader
    def load_user_from_request(request):
        return other_user

    # When
    response = client.get(
        url_for('user.order_detail', order_id=order.id))

    # Then
    assert response.status_code == 200
    template, _ = captured_templates[0]
    assert template.name == 'user/not_your_order.html.j2'


def test_orders(client, loginned_user, order, captured_templates):
    # When
    response = client.get(url_for('user.orders'))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'user/orders.html.j2'
    assert len(context['orders']) == 1
