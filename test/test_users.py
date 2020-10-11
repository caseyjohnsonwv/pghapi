import pytest
import env
from .startup import client

users_route = '/users'


"""
DUMMY TEST DATA
"""

class User:
    def __init__(self, name:str, phone:str):
        self.name = name
        self.phone = phone
    def to_json(self):
        return {"name":self.name,"phone":self.phone}
user1 = User("John Smith","1111111111")
user2 = User("Mary Carpenter","2222222222")


"""
TEST CASES BELOW
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
