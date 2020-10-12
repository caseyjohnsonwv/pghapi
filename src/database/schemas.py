from typing import List, Optional, Union
from pydantic import BaseModel

class LocationBase(BaseModel):
    address: str

class LocationUpdater(BaseModel):
    new_address: str
    class Config:
        orm_mode = True

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

class UserUpdater(BaseModel):
    new_phone: Optional[str] = None
    new_name: Optional[str] = None
    class config:
        orm_mode = True

class User(UserBase):
    id: int
    locations: List[UserLocation] = []
    class Config:
        orm_mode = True
