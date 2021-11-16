from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class Item(ItemBase):
    id: int
    owner_id: int


class UserBase(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    items: List[Item] = []
