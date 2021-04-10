from sqlalchemy.orm import relationship
from app import db

from .category import Category

category_products = db.Table('category_products', db.metadata,
                             db.Column('category_id', db.Integer,
                                       db.ForeignKey('category.id')),
                             db.Column('product_id', db.Integer,
                                       db.ForeignKey('product.id'))
                             )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    categories = relationship(
        Category, secondary=category_products, backref='products')
    detail = db.Column(db.String())
    image_url = db.Column(db.String())
