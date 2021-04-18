import abc
from .event import Event


class Handler(abc.ABC):
    @abc.abstractmethod
    def handle(self, event: Event):
        raise NotImplementedError
