
from sqlalchemy.orm import backref, relationship
from app import db
from app.catalog.domain.product import Product


class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    product = relationship(
        Product, backref=backref('order_line_set', lazy=True))
    quantity = db.Column(db.Integer)

    def get_amounts(self):
        return self.product.price * self.quantity
