import abc
from .product import Product
from .category import Category


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

    @abc.abstractmethod
    def find_by_category(self, category: Category, offset: int, limit: int):
        raise NotImplementedError

    @abc.abstractmethod
    def counts_by_category(self, category: Category):
        raise NotImplementedError
