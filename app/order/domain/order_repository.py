import abc
from .order import Order


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, order: Order):
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id: int):
        raise NotImplementedError
