from app.order.domain.order import Order
from app.order.domain.order_repository import OrderRepository


class SqlOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session

    def save(self, order: Order):
        self.session.add(order)
        self.session.commit()

    def find_all(self):
        return self.session.query(Order).all()

    def find_by_id(self, id: int):
        return self.session.query(Order).filter(Order.id == id).first()
