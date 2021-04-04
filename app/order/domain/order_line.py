from app import db
from sqlalchemy.orm import reconstructor, backref, relationship

class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = relationship('Product', backref=backref('order_line_set', lazy=True))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    amounts = db.Column(db.Integer)
    
    