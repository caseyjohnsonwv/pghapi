from typing import Optional, List
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import env
from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthcheck")
def get_healthcheck():
    return {"Status":"Alive"}


@app.get("/users", response_model=schemas.User)
def get_user(phone: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=409, detail="Phone already registered")
    return crud.create_user(db, user=user)


@app.get("/locations", response_model=schemas.Location)
def get_locations(address: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=address)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@app.post("/locations", response_model=schemas.Location)
def create_location(location: schemas.LocationBase, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=location.address)
    if db_location:
        raise HTTPException(status_code=409, detail="Location already created")
    return crud.create_location(db, location=location)


@app.get("/user-locations", response_model=List[schemas.UserLocation])
def get_user_locations(phone: str, nickname: Optional[str]=None, db: Session = Depends(get_db)):
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


@app.post("/user-locations", response_model=schemas.UserLocation)
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


if __name__ == '__main__':
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
