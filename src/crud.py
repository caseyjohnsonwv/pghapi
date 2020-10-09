from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(phone=user.phone, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_location_by_address(db: Session, address: str):
    return db.query(models.Location).filter(models.Location.address == address).first()

def create_location(db: Session, location: schemas.LocationBase):
    db_location = models.Location(address=location.address)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_user_locations_by_phone(db: Session, phone: str):
    user = get_user_by_phone(db, phone)
    if not user:
        return [None]
    return db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id).all() or [None]

def get_user_location_by_nickname_and_phone(db: Session, nickname: str, phone: str):
    user = get_user_by_phone(db, phone)
    if user:
        return db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id, models.UserLocation.nickname == nickname).first()

def get_user_location_by_address_and_phone(db: Session, address: str, phone: str):
    user = get_user_by_phone(db, phone)
    location = get_location_by_address(db, address)
    if user and location:
        return db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id, models.UserLocation.location_id == location.id).first()

def create_user_location(db: Session, user_location_creator: schemas.CreateUserLocation):
    user = get_user_by_phone(db, user_location_creator.phone)
    location = get_location_by_address(db, user_location_creator.address)
    db_user_location = models.UserLocation(user_id=user.id, location_id=location.id, nickname=user_location_creator.nickname)
    db.add(db_user_location)
    db.commit()
    db.refresh(db_user_location)
    return db_user_location
