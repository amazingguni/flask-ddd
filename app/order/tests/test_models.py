from datetime import datetime

from app.order.domain.order import Order
from app.order.domain.order_line import OrderLine
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address
from app.order.domain.order_state import OrderState

def test_order(db_session, orderer):
    shipping_info = ShippingInfo(
        receiver=Receiver('amazingguni', '000-000-0000'),
        address=Address('zip_code', 'suwon', 'seoul'),
        message='fast please'
        )
    order = Order(
        orderer=orderer,
        shipping_info=shipping_info,
        total_amounts=4000, state=OrderState.PREPARING,
        order_date=datetime.fromisoformat('2016-01-01 15:30:00')
        )
    db_session.add(order)
    db_session.commit()

def test_order_line_model(db_session, order):
    order_line = OrderLine(
        product_id='PRODUCT_1',
        price='100',
        quantity='4',
    )
    order_line.order = order
    db_session.add(order_line)
    db_session.commit()

    get_order_line = db_session.query(OrderLine).filter_by(product_id=order_line.product_id).first()
    assert get_order_line.product_id is order_line.product_id
