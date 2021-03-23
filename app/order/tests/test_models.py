
from app.order.domain.order import Order
from app.order.domain.orderer import Orderer
from app.order.domain.order_line import OrderLine
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address

def test_order(db_session):
    shipping_info = ShippingInfo(
        receiver=Receiver('amazingguni', '000-000-0000'),
        address=Address('zip_code', 'suwon', 'seoul'),
        message='fast please'
        )
    order = Order(
        orderer=Orderer(member_id='123', name='customer_A'),
        shipping_info=shipping_info
        )

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
