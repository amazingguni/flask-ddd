import abc
from .category import Category


class CategoryRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, category: Category):
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id: int):
        raise NotImplementedError
