from sqlalchemy.orm import Session
from fastapi import Depends
import pytest
import env
from main import get_db
from src import models
from .startup import client, engine
from src.database import Base

class Routes:
    h = '/healthcheck'
    u = '/users'
    l = '/locations'
    ul = '/user-locations'


"""DUMMY DATA"""

# users
John = models.User(name="John", phone="4126035678")
Mary = models.User(name="Mary", phone="3046764321")

# locations
PPG = models.Location(address="1 PPG Pl")
Heinz = models.Location(address="300 Heinz St")
Steelers = models.Location(address="100 Art Rooney Ave")

# automatically resets database between tests
@pytest.fixture(autouse=True)
def reset_database(db: Session = Depends(get_db)):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# for adding records to database before each test
def setup_database(db: Session = Depends(get_db), *argv):
    if argv:
        for arg in argv:
            db.add(arg)
        db.commit()


"""BEGIN TESTS"""

def test_healthcheck():
    route = Routes.h
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["Status"] == "Alive"

def create_user():
    route = Routes.u
    data = John.to_json()
    r = client.post(route, json=data)
    assert r.status == 200

def create_location():
    route = Routes.l
    data = PPG.to_json()
    r = client.post(route, json=data)
    assert r.status == 200

def create_user_location():
    setup_database(John, PPG)
    route = Routes.ul
    data = {"phone":John.phone, "address":PPG.address}
    r = client.post(route, json=data)
    assert r.status == 200
