from flask import url_for


def test_order_detail(db_session, client, captured_templates, loginned_user, order):
    # When
    response = client.get(
        url_for('user.order_detail', order_id=order.id))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'user/order_detail.html.j2'
    assert context['order'].id == order.id
