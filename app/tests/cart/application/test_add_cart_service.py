import pytest

from app.catalog.domain.product import Product

from app.cart.application.add_cart_service import AddCartService
from app.cart.domain.cart import Cart


@pytest.fixture(scope='function')
def add_cart_service(cart_repository):
    return AddCartService(cart_repository)


def test_add(db_session, add_cart_service, product, loginned_user):
    cart = Cart(
        product_id=product.id,
        quantity=2,
        user_id=loginned_user.id)

    # When
    add_cart_service.add(loginned_user, cart)

    # Then
    cart_query = db_session.query(Cart).filter(
        Cart.user_id == loginned_user.id)
    assert cart_query.count() == 1
    assert cart_query.first().quantity == 2


def test_add_GIVEN_existing_other_product(db_session, add_cart_service, product, loginned_user):
    # Given
    other_product = Product(
        name='다른 과자', price=2000, detail='음..')
    db_session.add(other_product)
    db_session.commit()
    other_cart = Cart(
        product_id=other_product.id,
        quantity=1,
        user_id=loginned_user.id)
    db_session.add(other_cart)
    db_session.commit()

    cart = Cart(
        product_id=product.id,
        quantity=2,
        user_id=loginned_user.id)

    # When
    add_cart_service.add(loginned_user, cart)

    # Then
    cart_query = db_session.query(Cart).filter(
        Cart.user_id == loginned_user.id, Cart.product_id == product.id)
    assert cart_query.count() == 1
    assert cart_query.first().quantity == 2


def test_add_GIVEN_existing_same_product_THEN_add_quantity(db_session, add_cart_service, product, loginned_user):
    # Given
    existing_cart = Cart(
        product_id=product.id,
        quantity=1,
        user_id=loginned_user.id)
    db_session.add(existing_cart)
    db_session.commit()

    cart = Cart(
        product_id=product.id,
        quantity=2,
        user_id=loginned_user.id)

    # When
    add_cart_service.add(loginned_user, cart)

    # Then
    cart_query = db_session.query(Cart).filter(
        Cart.user_id == loginned_user.id, Cart.product_id == product.id)
    assert cart_query.count() == 1
    assert cart_query.first().quantity == 3
