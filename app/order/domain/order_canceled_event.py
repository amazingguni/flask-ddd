
from app.common.event.event import Event


class OrderCanceledEvent(Event):
    def __init__(self, order_id):
        self.order_id = order_id
