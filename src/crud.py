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

def get_locations_by_user_phone(db: Session, phone: str):
    user = get_user_by_phone(db, phone)
    return db.query(models.Location).filter(models.Location.user_id == user.id).all()

def get_location_by_address(db: Session, address: str):
    return db.query(models.Location).filter(models.Location.address == address).first()

def get_location_by_nickname_and_phone(db: Session, nickname: str, phone: str):
    user = get_user_by_phone(db, phone)
    return db.query(models.Location).filter(models.Location.user_id == user.id, models.Location.nickname == nickname).first()

def create_location(db: Session, location: schemas.CreateLocation):
    user = get_user_by_phone(db, location.user_phone)
    db_location = models.Location(address=location.address, nickname=location.nickname, user_id=user.id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location
