from app import db
from sqlalchemy.orm import reconstructor

class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.String(128))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    
    