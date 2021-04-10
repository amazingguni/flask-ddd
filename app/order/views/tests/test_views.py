

from flask import url_for

from app.user.domain.user import User
from app.catalog.domain.product import Product

from app.tests import utils


def test_confirm(db_session, client, captured_templates, loginned_user):
    # Given
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')
    db_session.add(product)
    db_session.commit()

    # When
    response = client.get(
        url_for('order.confirm', quantity=1, product_id=product.id))

    # Then
    template, context = captured_templates[0]
    assert template.name == 'order/order_confirm.html.j2'
    assert context['orderer'] == loginned_user
    assert len(context['order_products']) == 1
    assert context['order_products'][0].product_id == product.id


def test_confirm_invalid_product_id():
    pass
