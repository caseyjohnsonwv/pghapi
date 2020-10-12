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


"""
DUMMY DATA

Using functions to avoid ObjectDeletedError on retest.
Only options are cumbersome functions or tightly-coupled tests.
"""

# users
def John():
    return models.User(name="John", phone="4126035678")
def Mary():
    return models.User(name="Mary", phone="3046764321")

# locations
def PPG():
    return models.Location(address="1 PPG() Pl")
def Heinz():
    Heinz = models.Location(address="300 Heinz St")
def Steelers():
    models.Location(address="100 Art Rooney Ave")

# automatically resets database between tests
@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# for adding records to database before each test
db = TestingSessionLocal()
def setup_database(*objects):
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
    data = John().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_location():
    route = Routes.l
    data = PPG().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_user_location():
    setup_database(John(), PPG())
    route = Routes.ul
    data = {"phone":John().phone, "address":PPG().address}
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_get_user():
    setup_database(John())
    route = "{route}?phone={phone}".format(route=Routes.u, phone=John().phone)
    data = John().to_json()
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["name"] == John().name
    assert r_json["phone"] == John().phone

def test_get_location():
    setup_database(PPG())
    route = "{route}?address={address}".format(route=Routes.l, address=PPG().address)
    data = PPG().to_json()
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["address"] == PPG().address

def test_get_user_location():
    setup_database(John(), PPG())
    ul_nickname = "Work"
    client.post(Routes.ul, json={"phone":John().phone,"address":PPG().address,"nickname":ul_nickname})
    route = "{route}?phone={phone}&nickname={nickname}".format(route=Routes.ul, phone=John().phone, nickname=ul_nickname)
    r = client.get(route)
    r_json = r.json()[0]
    assert r.status_code == 200
    assert r_json["phone"] == John().phone
    assert r_json["address"] == PPG().address
    assert r_json["nickname"] == ul_nickname
