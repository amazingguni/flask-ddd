from sqlalchemy.sql import func
from sqlalchemy.orm import composite, relationship, backref

from app import db, dispatcher

from app.user.domain.user import User
from .order_line import OrderLine
from .order_state import OrderState
from .shipping_info import ShippingInfo

from .exceptions import AlreadyShippedException
from .order_canceled_event import OrderCanceledEvent


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderer_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    orderer = relationship(User, backref=backref('order_set', lazy=True))

    order_lines = relationship(OrderLine, backref='order')
    # ShippingInfo
    # Receiver
    receiver_name = db.Column(db.String(128))
    receiver_phone = db.Column(db.String(128))
    # Address
    shipping_zip_code = db.Column(db.String(128))
    shipping_address1 = db.Column(db.String())
    shipping_address2 = db.Column(db.String())
    # Message
    shipping_message = db.Column(db.String())
    shipping_info = composite(ShippingInfo.generate,
                              receiver_name, receiver_phone,
                              shipping_zip_code, shipping_address1, shipping_address2,
                              shipping_message)

    state = db.Column(db.Enum(OrderState))
    order_date = db.Column(db.DateTime, server_default=func.now())

    def get_total_amounts(self):
        return sum([line.get_amounts() for line in self.order_lines])

    def cancel(self):
        self.verify_not_yet_shipped()
        self.state = OrderState.CANCELED
        dispatcher.dispatch(OrderCanceledEvent(order_id=self.id))

    def verify_not_yet_shipped(self):
        if not self.is_not_yet_shipped():
            raise AlreadyShippedException

    def is_not_yet_shipped(self):
        return self.state == OrderState.PAYMENT_WAITING or \
            self.state == OrderState.PREPARING
