import abc
from app.user.domain.user import User
from .cart import Cart


class CartRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, cart: Cart):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_user(self, user: User):
        raise NotImplementedError
