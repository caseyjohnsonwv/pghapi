from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import crud, models, schemas
from main import get_db

router = APIRouter()


@router.get("/", response_model=schemas.Location)
def get_locations(address: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=address)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationBase, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=location.address)
    if db_location:
        raise HTTPException(status_code=409, detail="Location already created")
    return crud.create_location(db, location=location)


@router.delete("/", response_model=None)
def delete_location(address: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_address(db, address=address)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    try:
        return crud.delete_location(db, location=db_location)
    except AssertionError as ex:
        raise HTTPException(status_code=409, detail="Location cannot be deleted")
