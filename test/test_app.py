import pytest
import env
from .startup import client

users_route = '/users'
locations_route = '/locations'


"""
DUMMY TEST DATA
"""

class User:
    def __init__(self, name:str, phone:str):
        self.name = name
        self.phone = phone
    def to_json(self):
        return {"name":self.name,"phone":self.phone}
user1 = User(name="John Smith", phone="1111111111")
user2 = User(name="Mary Carpenter", phone="2222222222")

class Location:
    def __init__(self, address:str):
        self.address = address
    def to_json(self):
        return {"address":self.address}
location1 = Location(address="210 Sixth Avenue, Pittsburgh, PA 15222")
location2 = Location(address="1 PPG Place, Pittsburgh, PA 15222")

"""
STARTUP TESTS
"""

def test_healthcheck():
    route = "/healthcheck"
    r = client.get(route)
    assert r.status_code == 200
    assert r.json() == {"Status":"Alive"}


"""
USER TESTS
"""

def test_create_user_missing_name():
    # expect 422 unprocessable entity
    route = users_route
    data = user1.to_json()
    del data["name"]
    r = client.post(route, json=data)
    assert r.status_code == 422

def test_create_user_missing_phone():
    # expect 422 unprocesseable entity
    route = users_route
    data = user1.to_json()
    del data["phone"]
    r = client.post(route, json=data)
    assert r.status_code == 422

def test_create_user():
    # expect 200 ok
    route = users_route
    data = user1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_existing_user():
    # expect 400 already created
    route = users_route
    data = user1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 400

def test_get_user():
    # expect 200 ok + data matches
    route = "{route}?phone={phone}".format(route=users_route, phone=user1.phone)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["phone"] == user1.phone
    assert r_json["name"] == user1.name

def test_get_nonexistent_user():
    # expect 404 not found
    route = "{route}?phone={phone}".format(route=users_route, phone=user2.phone)
    r = client.get(route)
    assert r.status_code == 404


"""
LOCATION TESTS
"""

def test_create_location():
    # expect 200 ok
    route = locations_route
    data = location1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_existing_location():
    # expect 400 already exists
    route = locations_route
    data = location1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 400

def test_get_location():
    # expect 200 ok + matching data
    route = "{route}?address={address}".format(route=locations_route, address=location1.address)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["address"] == location1.address

def test_get_nonexistent_location():
    # expect 404 not found
    route = "{route}?address={address}".format(route=locations_route, address=location2.address)
    r = client.get(route)
    assert r.status_code == 404
