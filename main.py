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
        raise HTTPException(status_code=400, detail="Phone already registered")
    return crud.create_user(db, user=user)

@app.get("/locations", response_model=List[schemas.Location])
def get_location(phone: str, nickname: Optional[str]=None, address: Optional[str]=None, db: Session = Depends(get_db)):
    if address:
        locations = [crud.get_location_by_address(db, address=address)]
    elif nickname:
        locations = [crud.get_location_by_nickname_and_phone(db, nickname=nickname, phone=phone)]
    else:
        locations = crud.get_locations_by_user_phone(db, phone=phone)
    if not locations:
        raise HTTPException(status_code=404, detail="Location(s) not found")
    return locations

@app.post("/locations", response_model=schemas.Location)
def create_location(location: schemas.CreateLocation, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=location.address)
    if db_location:
        raise HTTPException(status_code=400, detail="Location already created")
    return crud.create_location(db, location=location)

if __name__ == '__main__':
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
