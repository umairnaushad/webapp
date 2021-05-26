from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, true
from base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=true)
    email = Column(String(120), nullable=true)
    ##email = Column(String(120), unique=false, nullable=true)
    def __init__(self, username, email):
           self.username=username
           self.email=email

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }