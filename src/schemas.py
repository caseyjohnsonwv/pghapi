from typing import List, Optional
from pydantic import BaseModel

class LocationBase(BaseModel):
    address: str

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True


class UserLocation(BaseModel):
    location_id: int
    user_id: int
    nickname: Optional[str] = None
    class Config:
        orm_mode = True

class CreateUserLocation(BaseModel):
    address: str
    phone: str
    nickname: Optional[str] = None
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    phone: str
    name: str

class User(UserBase):
    id: int
    locations: List[UserLocation] = []
    class Config:
        orm_mode = True
