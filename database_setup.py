import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    uid = Column(Integer, primary_key=True)
    email = Column(String(45), nullable=False)
    pword = Column(String(45), nullable=False)
    fname = Column(String(45), nullable=False)
    lname = Column(String(45), nullable=False)
    street_addr = Column(String(45), nullable=False)
    cid = Column(Integer, nullable=False,ForeignKey('City.cid'))
    uprofile = Column(String(140), nullable=True)
    photo = Column(String(45))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(65536))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)