from sqlalchemy.orm import Session
import pytest
import env
from src import models
from .startup import client, engine, TestingSessionLocal
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
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# for adding records to database before each test
def setup_database(*objects):
    db = TestingSessionLocal()
    if objects:
        for obj in objects:
            db.add(obj)
        db.commit()


"""BEGIN TESTS"""

def test_healthcheck():
    route = Routes.h
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["Status"] == "Alive"

def test_create_user():
    route = Routes.u
    data = John.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_location():
    route = Routes.l
    data = PPG.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_user_location():
    setup_database(John, PPG)
    route = Routes.ul
    data = {"phone":John.phone, "address":PPG.address}
    r = client.post(route, json=data)
    assert r.status_code == 200
