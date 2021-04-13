from ...domain.order import Order
from ...domain.order_repository import OrderRepository


class SqlOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session

    def save(self, order: Order):
        self.session.add(order)
        self.session.commit()

    def find_all(self):
        pass

    def find_by_id(self, id: int):
        pass
