from sqlalchemy_utils import create_view
from app import db
from app.order.domain.order import Order
from app.order.domain.order_line import OrderLine
from app.catalog.domain.product import Product

class OrderSummary(db.Model):
        __table__ = create_view(
            name='order_summary',
            selectable=db.select(
                [
                    Order.id,
                    Order.orderer_id,
                    Order.orderer_name,
                ],
                from_obj=(
                    Order.__table__.join(OrderLine, Order.id == OrderLine.order_id)
                )
            ),
            metadata=db.Model.metadata
        )