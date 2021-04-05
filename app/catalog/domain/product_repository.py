import abc
from .product import Product


class ProductRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, product: Product):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_by_id(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id: int):
        raise NotImplementedError
