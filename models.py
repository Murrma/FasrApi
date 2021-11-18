from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(200))

    item = relationship("Item", back_populates="user", uselist=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "{} {} {}".format(self.id, self.email, self.password)

    def serialize(self):
        return {"data": self.id,
                "password": self.password,
                "email": self.email}


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="item")

    def __init__(self, title, description, owner_id):
        self.title = title
        self.description = description
        self.owner_id = owner_id

    def __repr__(self):
        return "{} {} {}".format(self.id, self.title, self.description, self.owner_id)

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "owner_id": self.owner_id}
