from app.user.domain.user import User
from app.cart.domain.cart import Cart
from app.cart.infra.repository.sql_cart_repository import SqlCartRepository


def test_save(db_session, loginned_user, product):
    # Given
    cart = Cart(
        user=loginned_user,
        product=product,
        quantity=5
    )

    # When
    SqlCartRepository(db_session).save(cart)

    # Then
    assert db_session.query(Cart).count() == 1


def test_find_by_user(db_session, loginned_user, product):
    # Given
    cart = Cart(
        user=loginned_user,
        product=product,
        quantity=5
    )
    db_session.add(cart)

    # When
    carts = SqlCartRepository(db_session).find_by_user(loginned_user)

    # Then
    assert len(carts) == 1


def test_find_by_user_GIVEN_other_user_THEN_nothing(db_session, loginned_user, product):
    # Given
    cart = Cart(
        user=loginned_user,
        product=product,
        quantity=5
    )
    db_session.add(cart)
    other_user = User(username='other_user', password='1234')

    # When
    carts = SqlCartRepository(db_session).find_by_user(other_user)

    # Then
    assert len(carts) == 0


def test_delete_by_user(db_session, loginned_user, product):
    cart = Cart(
        user=loginned_user,
        product=product,
        quantity=5
    )
    db_session.add(cart)
    assert db_session.query(Cart).count() == 1

    # When
    SqlCartRepository(db_session).delete_by_user(loginned_user)

    # Then
    assert db_session.query(Cart).count() == 0
