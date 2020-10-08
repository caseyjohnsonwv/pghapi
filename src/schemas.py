from typing import List, Optional
from pydantic import BaseModel


class LocationBase(BaseModel):
    address: str
    nickname: Optional[str] = None

class CreateLocation(LocationBase):
    user_phone: str

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    phone: str
    name: str

class User(UserBase):
    id: int
    locations: List[Location] = []
    class Config:
        orm_mode = True
