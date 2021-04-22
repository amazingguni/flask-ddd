
from sqlalchemy.orm import backref, relationship
from app import db
from app.user.domain.user import User
from app.catalog.domain.product import Product


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    user = relationship(User, backref=backref('cart_set', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    product = relationship(
        Product, backref=backref('cart_set', lazy=True))
    quantity = db.Column(db.Integer)

    def get_amounts(self):
        return self.product.price * self.quantity
