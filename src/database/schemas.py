from typing import List, Optional, Union
from pydantic import BaseModel, validator

class LocationBase(BaseModel):
    address: str

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True


class UserLocationBase(BaseModel):
    nickname: Optional[str] = None

class UserLocationRef(UserLocationBase):
    user_id: int
    location_id: int
    class Config:
        orm_mode = True

class UserLocation(UserLocationBase):
    address: str
    phone: str
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
