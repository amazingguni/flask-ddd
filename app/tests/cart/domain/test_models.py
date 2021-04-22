from app.cart.domain.cart import Cart


def test_cart(db_session, loginned_user, product):
    cart = Cart(product=product, quantity=4, user=loginned_user)
    db_session.add(cart)
    db_session.commit()

    get_cart = db_session.query(Cart).filter_by(
        product=product, quantity=4, user=loginned_user
    ).first()
    assert get_cart.id is cart.id
