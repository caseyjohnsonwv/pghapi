from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database import crud, models, schemas

router = APIRouter()

from main import get_db

@router.get("/", response_model=schemas.User)
def read_user(phone: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=409, detail="Phone already registered")
    return crud.create_user(db, user=user)


@router.delete("/", response_model=None)
def delete_user(phone: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user=db_user)

@router.patch("/", response_model=schemas.User)
def update_user(phone: str, payload: schemas.UserUpdater, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if payload.new_name:
        return crud.update_user_name(db, user=db_user, new_name=payload.new_name)
    elif payload.new_phone:
        try:
            return crud.update_user_phone(db, user=db_user, new_phone=payload.new_phone)
        except IntegrityError as ex:
            raise HTTPException(status_code=409, detail="Phone already registered")
    else:
        raise HTTPException(status_code=400, detail="No update data supplied")
