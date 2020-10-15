import re
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, validator


def _validate_phone(v: str):
    simple_phone_regex = r"(?:\d{3}|\(\d{3}\))[\s\-\.]?\d{3}[\s\-\.]?\d{4}"
    if not re.match(simple_phone_regex, v):
        raise ValueError("Invalid phone number")
    return v
def phone_validator(field:str):
    decorator = validator(field, allow_reuse=True, check_fields=False)
    function = decorator(_validate_phone)
    return function


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
    _phone_validator: classmethod = phone_validator('phone')


class UserBase(BaseModel):
    phone: str
    name: str
    _phone_validator: classmethod = phone_validator('phone')

class UserUpdater(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    preferences: Optional[Dict] = {}
    class Config:
        orm_mode = True
    _phone_validator: classmethod = phone_validator('phone')

class User(UserBase):
    id: int
    preferences: Dict
    locations: List[UserLocation] = []
    class Config:
        orm_mode = True


class TravelTime(BaseModel):
    origin: str
    destination: str
    time_estimate: str
    class Config:
        orm_mode = True
