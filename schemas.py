from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    owner_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Item(ItemBase):
    id: int


class UserBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class User(UserBase):
    id: int
    #item: List[Item] = []
