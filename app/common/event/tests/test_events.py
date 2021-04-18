from ..event_dispatcher import EventDispatcher
from ..event import Event
from ..handler import Handler


class CustomEvent(Event):
    def __init__(self, message):
        self.message = message


class OtherEvent(Event):
    pass


class CustomHandler(Handler):
    def __init__(self):
        self.called = False

    def handle(self, event: CustomEvent):
        self.called = True
        self.event = event


def test_handle():
    dispather = EventDispatcher()
    handler = CustomHandler()
    dispather.register(CustomEvent, handler)

    # When
    dispather.dispatch(CustomEvent('lets go!'))

    # Then
    assert handler.called == True
    assert handler.event.message == 'lets go!'


def test_handle_WHEN_other_event_THEN_nothing():
    dispather = EventDispatcher()
    handler = CustomHandler()
    dispather.register(CustomEvent, handler)

    # When
    dispather.dispatch(OtherEvent())

    # Then
    assert handler.called == False


def test_reset():
    dispather = EventDispatcher()
    handler = CustomHandler()
    dispather.register(CustomEvent, handler)

    # When
    dispather.reset()

    # Then
    dispather.dispatch(CustomEvent('lets go!'))
    assert handler.called == False
