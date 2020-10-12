from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    locations = relationship("UserLocation")

    def to_json(id=False, locations=False):
        j = {"phone":phone, "name":name}
        if id:
            j["id"] = id
        if locations:
            j["locations"] = locations
        return j


class UserLocation(Base):
    __tablename__ = "user_locations"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    nickname = Column(String)

    def to_json():
        return {"user_id":user_id, "location_id":location_id, "nickname":nickname}


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True, nullable=False)

    def to_json(id=False):
        j = {"address":address}
        if id:
            j["id"] = id
        return j
