from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    email = Column(String, unique=True)


class Item(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, unique=True)
    total = Column(String, unique=True)