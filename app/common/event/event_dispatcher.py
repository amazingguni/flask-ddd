from collections import defaultdict
from typing import Type
from .event import Event
from .handler import Handler


class EventDispatcher:
    def __init__(self):
        self.__dispatch_map = defaultdict(list)

    def register(self, event: Type[Event], handler: Handler):
        self.__dispatch_map[event].append(handler)

    def dispatch(self, event: Type[Event]):
        for handler in self.__dispatch_map[type(event)]:
            handler.handle(event)

    def reset(self):
        self.__dispatch_map.clear()
