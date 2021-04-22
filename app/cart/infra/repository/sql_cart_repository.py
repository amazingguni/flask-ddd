from app.user.domain.user import User

from app.cart.domain.cart import Cart
from app.cart.domain.cart_repository import CartRepository


class SqlCartRepository(CartRepository):
    def __init__(self, session):
        self.session = session

    def save(self, cart: Cart):
        self.session.add(cart)
        self.session.commit()

    def find_by_user(self, user: User):
        return self.session.query(Cart).filter(Cart.user_id == user.id).all()

    def delete_by_user(self, user: User):
        self.session.query(Cart).filter(Cart.user_id == user.id).delete()
