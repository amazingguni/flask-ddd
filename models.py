from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<id {}>'.format(self.id)