import re
from typing import List, Optional
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
    allow_tolls: Optional[bool] = None
    allow_highways: Optional[bool] = None
    allow_ferries: Optional[bool] = None
    class Config:
        orm_mode = True
    _phone_validator: classmethod = phone_validator('phone')

class User(UserBase):
    id: int
    allow_tolls: bool
    allow_highways: bool
    allow_ferries: bool
    locations: List[UserLocation] = []
    class Config:
        orm_mode = True


class TravelTime(BaseModel):
    destinations: List[str]
    time_estimates: List[int]
    class Config:
        orm_mode = True
    @validator('time_estimates')
    def _validate_traveltime_response(time_estimates: List[int]):
        if len(destinations)-1 != len(time_estimates):
            raise ValueError("Must be one more address than time estimates")
        return time_estimates
