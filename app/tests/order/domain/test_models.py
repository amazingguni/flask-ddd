from datetime import datetime

from app.order.domain.order import Order
from app.order.domain.order_line import OrderLine
from app.order.domain.order_state import OrderState


def test_order(db_session, loginned_user, shipping_info):
    order = Order(
        orderer=loginned_user,
        shipping_info=shipping_info,
        state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-01 15:30:00')
    )
    db_session.add(order)
    db_session.commit()


def test_order_line_model(db_session, product, order):
    order_line = OrderLine(
        product=product,
        quantity='4',
    )
    order.order_lines.append(order_line)
    db_session.add(order)
    db_session.commit()

    get_order_line = db_session.query(OrderLine).filter_by(
        product_id=order_line.product_id).first()
    assert get_order_line.product_id is order_line.product_id
