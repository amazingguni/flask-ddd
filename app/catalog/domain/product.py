from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    detail = db.Column(db.String())