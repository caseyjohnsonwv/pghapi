from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    allow_tolls = Column(Boolean, default=True)
    allow_highways = Column(Boolean, default=True)
    allow_ferries = Column(Boolean, default=True)
    userlocations = relationship("UserLocation", cascade="all, delete")

    def to_json(self, id=False, locations=False, preferences=False):
        j = {
            "phone":self.phone,
            "name":self.name,
        }
        if self.id:
            j["id"] = self.id
        if self.userlocations:
            j["user_locations"] = self.userlocations
        if preferences:
            j["allow_tolls"] = self.allow_tolls
            j["allow_highways"] = self.allow_highways
            j["allow_ferries"] = self.allow_ferries
        return j


class UserLocation(Base):
    __tablename__ = "user_locations"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    nickname = Column(String)

    def to_json(self):
        return {"user_id":self.user_id, "location_id":self.location_id, "nickname":self.nickname}


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True, nullable=False)
    userlocations = relationship("UserLocation")

    def to_json(self, id=False):
        j = {"address":self.address}
        if self.id:
            j["id"] = self.id
        return j
