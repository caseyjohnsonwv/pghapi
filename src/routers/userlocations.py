from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import crud, models, schemas

router = APIRouter()

from main import get_db


@router.get("/", response_model=List[schemas.UserLocation])
def read_user_locations(phone: str, nickname: Optional[str]=None, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if nickname:
        locations = [crud.get_user_location_by_nickname_and_phone(db, nickname=nickname, phone=phone)]
    else:
        locations = crud.get_user_locations_by_phone(db, phone=phone)
    if not locations[0]:
        raise HTTPException(status_code=404, detail="User location(s) not found")
    return locations


@router.post("/", response_model=schemas.UserLocation)
def create_user_location(user_location_creator: schemas.UserLocation, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user_location_creator.phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_location = crud.get_location_by_address(db, address=user_location_creator.address)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db_user_location = crud.get_user_location_by_user_and_location(db, user=db_user, location=db_location)
    if db_user_location:
        raise HTTPException(status_code=409, detail="User location already created")
    out = crud.create_user_location(db, user=db_user, location=db_location, nickname=user_location_creator.nickname)
    return out

@router.delete("/", response_model=None)
def delete_user_location(phone: str, address: Optional[str] = None, nickname: Optional[str] = None, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if address:
        db_location = crud.get_location_by_address(db, address=address)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location not found")
        db_user_location = crud.get_user_location_by_user_and_location(db, user=db_user, location=db_location)
    elif nickname:
        db_user_location = crud.get_user_location_by_nickname_and_phone(db, nickname=nickname, phone=phone)
    else:
        raise HTTPException(status_code=422, detail="Address or nickname required")
    if not db_user_location:
        raise HTTPException(status_code=404, detail="User location not found")
    return crud.delete_user_location(db, user_location=db_user_location)

if __name__ == '__main__':
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
