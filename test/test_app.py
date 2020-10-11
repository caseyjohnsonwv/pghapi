import pytest
import env
from .startup import client

users_route = '/users'
locations_route = '/locations'
user_locations_route = '/user-locations'


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
location3 = Location(address="1200 Penn Ave, Pittsburgh, PA 15222")

class UserLocation:
    def __init__(self, phone:str, address:str, nickname:str = None):
        self.phone = phone
        self.address = address
        self.nickname = nickname
    def to_json(self):
        data = {"phone":self.phone,"address":self.address}
        if self.nickname:
            data["nickname"] = self.nickname
        return data
user1_location1 = UserLocation(phone=user1.phone, address=location1.address)
user1_location2 = UserLocation(phone=user1.phone, address=location2.address, nickname="Location 2")
user1_location3 = UserLocation(phone=user1.phone, address=location3.address, nickname="User 1 Home")
user2_location1 = UserLocation(phone=user2.phone, address=location1.address)
user2_location2 = UserLocation(phone=user2.phone, address=location2.address, nickname="Location 2")


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
    # expect 422 unprocessable entity
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
    # create user for later testing
    route = users_route
    data = user2.to_json()
    client.post(route, json=data)


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
    # create locations for later testing
    route = locations_route
    for l in [location2, location3]:
        data = l.to_json()
        client.post(route, json=data)


"""
USER LOCATION TESTS
"""

def test_create_user_location_missing_phone():
    # expect 422 unprocessable entity
    route = user_locations_route
    data = user1_location1.to_json()
    del data["phone"]
    r = client.post(route, json=data)
    assert r.status_code == 422

def test_create_user_location_missing_address():
    # expect 422 unprocessable entity
    route = user_locations_route
    data = user1_location1.to_json()
    del data["address"]
    r = client.post(route, json=data)
    assert r.status_code == 422

def test_create_user_location_no_nickname():
    # expect 200 ok
    route = user_locations_route
    data = user1_location1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_user_location_with_nickname():
    # expect 200 ok
    route = user_locations_route
    data = user1_location2.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_existing_user_location():
    # expect 400 already exists
    route = user_locations_route
    data = user1_location1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 400

def test_create_user_location_different_user_same_address():
    # expect 200 ok
    route = user_locations_route
    data = user2_location1.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_create_user_location_different_user_same_nickname():
    # expect 200 ok
    route = user_locations_route
    data = user2_location2.to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200

def test_get_user_location_missing_phone():
    # expect 422 unprocessable entity
    route = "{route}?nickname={nickname}".format(route=user_locations_route, nickname=user1_location1.nickname)
    r = client.get(route)
    assert r.status_code == 422

def test_get_user_location_with_nickname():
    # expect 200 ok + matching data
    route = "{route}?phone={phone}&nickname={nickname}".format(route=user_locations_route, phone=user1_location2.phone, nickname=user1_location2.nickname)
    r = client.get(route)
    r_json = r.json()[0]
    assert r.status_code == 200
    assert r_json["phone"] == user1_location2.phone
    assert r_json["address"] == user1_location2.address
    assert r_json["nickname"] == user1_location2.nickname

def test_get_nonexistent_user_location():
    # expect 404 not found
    route = "{route}?phone={phone}&nickname={nickname}".format(route=user_locations_route, phone=user1_location1.phone, nickname="A7f5bnIx30f")
    r = client.get(route)
    assert r.status_code == 404

def test_get_user_location_belonging_to_another_user():
    # expect 404 not found
    # create user location for user 1's home
    route = user_locations_route
    data = user1_location3.to_json()
    client.post(route, json=data)
    # try to access it as user 2
    route = "{route}?phone={phone}&nickname={nickname}".format(route=user_locations_route, phone=user2.phone, nickname="User 1 Home")
    r = client.get(route)
    assert r.status_code == 404

def test_get_all_locations_of_user():
    # expect 200 ok + matching data
    route = "{route}?phone={phone}".format(route=user_locations_route, phone=user1.phone)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    for ul in r_json:
        assert ul["phone"] == user1.phone
