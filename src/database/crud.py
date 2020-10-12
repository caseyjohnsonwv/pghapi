from sqlalchemy.orm import Session
from . import models, schemas


class CrudUtils:
    def user_location_ref_to_readable(db: Session, ref: schemas.UserLocationRef):
        if ref:
            user = db.query(models.User).filter(models.User.id == ref.user_id).first()
            location = db.query(models.Location).filter(models.Location.id == ref.location_id).first()
            return {"phone":user.phone,"address":location.address,"nickname":ref.nickname}
    def user_location_readable_to_ref(db: Session, readable: schemas.UserLocation):
        if readable:
            user = db.query(models.User).filter(models.User.phone == readable["phone"]).first()
            location = db.query(models.Location).filter(models.Location.address == readable["address"]).first()
            return {"user_id":user.id, "location_id":location.id,"nickname":readable["nickname"]}


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(phone=user.phone, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db.delete(db_user)
    db.commit()


def get_location_by_address(db: Session, address: str):
    return db.query(models.Location).filter(models.Location.address == address).first()

def create_location(db: Session, location: schemas.LocationBase):
    db_location = models.Location(address=location.address)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def delete_location(db: Session, location: schemas.Location):
    db_location = db.query(models.Location).filter(models.Location.id == location.id).first()
    db.delete(db_location)
    db.commit()


def get_user_locations_by_phone(db: Session, phone: str):
    user = get_user_by_phone(db, phone=phone)
    refs = db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id).all()
    out = []
    for ref in refs:
        out.append(CrudUtils.user_location_ref_to_readable(db, ref=ref))
    return out

def get_user_location_by_nickname_and_phone(db: Session, nickname: str, phone: str):
    user = get_user_by_phone(db, phone=phone)
    ref = db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id, models.UserLocation.nickname == nickname).first()
    return CrudUtils.user_location_ref_to_readable(db, ref=ref)

def get_user_location_by_address_and_phone(db: Session, address: str, phone: str):
    user = get_user_by_phone(db, phone=phone)
    location = get_location_by_address(db, address=address)
    ref = db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id, models.UserLocation.location_id == location.id).first()
    return CrudUtils.user_location_ref_to_readable(db, ref=ref)

def get_user_location_by_user_and_location(db: Session, user: schemas.User, location: schemas.Location):
    ref = db.query(models.UserLocation).filter(models.UserLocation.user_id == user.id, models.UserLocation.location_id == location.id).first()
    return CrudUtils.user_location_ref_to_readable(db, ref=ref)

def create_user_location(db: Session, user: schemas.User, location: schemas.Location, nickname:str = None):
    db_user_location = models.UserLocation(user_id=user.id, location_id=location.id, nickname=nickname)
    db.add(db_user_location)
    db.commit()
    db.refresh(db_user_location)
    return get_user_location_by_user_and_location(db, user=user, location=location)

def delete_user_location(db: Session, user_location: schemas.UserLocation):
    ref = CrudUtils.user_location_readable_to_ref(db, readable=user_location)
    db_user_location = db.query(models.UserLocation).filter(
        models.UserLocation.user_id == ref["user_id"],
        models.UserLocation.location_id == ref["location_id"]
    ).first()
    db.delete(db_user_location)
    db.commit()
