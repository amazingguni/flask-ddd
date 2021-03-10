import datetime
from sqlalchemy.orm import composite
from sqlalchemy.sql import text
from sqlalchemy.sql import func
from app import db

from .orderer import Orderer
from .shipping_info import ShippingInfo

class Order(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    
    # Orderer
    orderer_id = db.Column(db.String(128))
    orderer_name = db.Column(db.String(128))
    orderer = composite(Orderer, orderer_id, orderer_name)

    # ShippingInfo
    ## Receiver
    receiver_name = db.Column(db.String(128))
    receiver_phone = db.Column(db.String(128))
    ## Address
    shipping_zip_code = db.Column(db.String(128))
    shipping_address1 = db.Column(db.String())
    shipping_address2 = db.Column(db.String())
    ## Message
    shipping_message = db.Column(db.String())
    shipping_info = composite(ShippingInfo._generate, \
        receiver_name, receiver_phone, \
        shipping_zip_code, shipping_address1, shipping_address2, \
        shipping_message)

    # order_lines = db.relationship('OrderLine', backref='order', lazy=True)
    # name = db.Column(db.String(128))
    total_amounts = db.Column(db.Integer)

    order_date = db.Column(db.DateTime, server_default=func.now())


    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<id {}>'.format(self.id)