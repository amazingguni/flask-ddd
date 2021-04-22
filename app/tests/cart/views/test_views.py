from flask import url_for

from app.catalog.domain.product import Product
from app.cart.domain.cart import Cart

from app.tests import utils


def test_add(db_session, client, captured_templates, loginned_user):
    # Given
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')

    db_session.add(product)
    db_session.commit()

    # When
    response = client.post(url_for('cart.add_cart'), data={
        'product_id': product.id,
        'quantity': 2
    })

    # Then
    utils.assert_redirect_response(response, url_for('cart.confirm'))
    assert db_session.query(Cart).count() == 1
    assert db_session.query(Cart).first().product_id == product.id
    assert db_session.query(Cart).first().quantity == 2


def test_confirm(db_session, client, captured_templates, loginned_user):
    # Given
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')
    db_session.add(product)
    db_session.commit()
    cart = Cart(product_id=product.id, quantity=1, user_id=loginned_user.id)
    db_session.add(cart)
    db_session.commit()

    # When
    response = client.get(url_for('cart.confirm'))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'cart/order_confirm.html.j2'
    assert context['orderer'] == loginned_user
    assert len(context['carts']) == 1
    assert context['carts'][0].product_id == product.id
