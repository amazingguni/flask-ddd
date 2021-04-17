from app.order.query.dao.order_summary_dao import OrderSummaryDao
from app.order.domain.order import Order
from app.order.query.dto.order_summary import OrderSummary


class SqlOrderSummaryDao(OrderSummaryDao):
    def __init__(self, session):
        self.session = session

    def select_by_orderer(self, orderer_id: int):
        orders = self.session.query(Order).filter(
            Order.orderer_id == orderer_id).all()
        return list(map(self._order_to_order_summary, orders))

    def counts(self, filters: dict):
        query = self.session.query(Order)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Order, attr) == value)
        return query.count()

    def select(self, filters: dict, offset: int, limit: int):
        query = self.session.query(Order)
        if filters:
            for attr, value in filters.items():
                query = query.filter(getattr(Order, attr) == value)
        return query.offset(offset).limit(limit).all()

    def _order_to_order_summary(self, order):
        return OrderSummary(
            order_id=order.id,
            orderer_id=order.orderer.id,
            orderer_username=order.orderer.username,
            total_amounts=order.get_total_amounts(),
            receiver_name=order.shipping_info.receiver.name,
            state=order.state,
            order_date=order.order_date,
            product_id=order.order_lines[0].product.id,
            product_name=order.order_lines[0].product.name,
        )
