from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class _UserPrefs(Enum):
    allow_tolls = "allow_tolls"
    allow_highways = "allow_highways"
    allow_ferries = "allow_ferries"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    preferences = Column(PickleType, nullable=False, default={item:True for item in _UserPrefs})
    userlocations = relationship("UserLocation", cascade="all, delete")

    def to_json(self):
        j = self.__dict__
        j.pop('_sa_instance_state')
        return j


class UserLocation(Base):
    __tablename__ = "user_locations"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    nickname = Column(String)

    def to_json(self):
        j = self.__dict__
        j.pop('_sa_instance_state')
        return j


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True, nullable=False)
    userlocations = relationship("UserLocation")

    def to_json(self):
        j = self.__dict__
        j.pop('_sa_instance_state')
        return j
