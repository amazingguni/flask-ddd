from sqlalchemy import Boolean, Column, Integer, \
    String
from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    blocked = Column(Boolean(255), default=False)
    is_admin = Column(Boolean(255), default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<username - {}>'.format(self.username)
