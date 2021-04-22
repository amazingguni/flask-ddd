
from app.user.domain.user import User

from app.cart.domain.cart_repository import CartRepository
from app.cart.domain.cart import Cart


class AddCartService:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def add(self, user: User, cart: Cart):
        carts = self.cart_repository.find_by_user(user)
        for existing_cart in carts:
            if existing_cart.product_id != cart.product_id:
                continue
            existing_cart.quantity += cart.quantity
            self.cart_repository.save(existing_cart)
            return
        self.cart_repository.save(cart)
