import pytest
import env
from src.database import models
from .startup import client, engine, TestingSessionLocal
from src.database.database import Base
from main import Routes


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
    return models.Location(address="1 PPG Pl")
def Heinz():
    return models.Location(address="300 Heinz St")
def Steelers():
    return models.Location(address="100 Art Rooney Ave")

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


"""
BEGIN TESTS

Tests are roughly sorted by database model and HTTP protocol.
"""

def test_healthcheck():
    route = Routes.healthcheck
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["Status"] == "Alive"


"""
CREATE USER TESTS
"""

def test_create_user():
    route = Routes.users
    data = John().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200


def test_create_existing_user():
    setup_database(John())
    route = Routes.users
    data = John().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 409


def test_create_user_no_name():
    route = Routes.users
    data = John().to_json()
    del data["name"]
    r = client.post(route, json=data)
    assert r.status_code == 422


def test_create_user_no_phone():
    route = Routes.users
    data = John().to_json()
    del data["phone"]
    r = client.post(route, json=data)
    assert r.status_code == 422


"""
CREATE LOCATION TESTS
"""

def test_create_location():
    route = Routes.locations
    data = PPG().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 200


def test_create_existing_location():
    setup_database(PPG())
    route = Routes.locations
    data = PPG().to_json()
    r = client.post(route, json=data)
    assert r.status_code == 409


def test_create_location_no_address():
    route = Routes.locations
    data = PPG().to_json()
    del data["address"]
    r = client.post(route, json=data)
    assert r.status_code == 422


"""
CREATE USERLOCATION TESTS
"""

def test_create_user_location():
    setup_database(John(), PPG())
    route = Routes.userlocations
    data = {"phone":John().phone, "address":PPG().address}
    r = client.post(route, json=data)
    assert r.status_code == 200


def test_create_existing_user_location():
    setup_database(John(), PPG())
    route = Routes.userlocations
    # create user location first
    data = {"phone":John().phone, "address":PPG().address}
    r = client.post(route, json=data)
    # then try to create it again
    r = client.post(route, json=data)
    assert r.status_code == 409


def test_create_user_location_no_phone():
    setup_database(John(), PPG())
    route = Routes.userlocations
    data = {"address":PPG().address}
    r = client.post(route, json=data)
    assert r.status_code == 422


def test_create_user_location_no_address():
    setup_database(John(), PPG())
    route = Routes.userlocations
    data = {"phone":John().phone}
    r = client.post(route, json=data)
    assert r.status_code == 422

def test_create_multiple_user_locations():
    setup_database(John(), PPG(), Heinz())
    route = Routes.userlocations
    addresses = [PPG().address, Heinz().address]
    for address in addresses:
        data = {"phone":John().phone,"address":address}
        r = client.post(route, json=data)
        r_json = r.json()
        assert r.status_code == 200
        assert r_json["phone"] == John().phone
        assert r_json["address"] == address

def test_create_user_location_different_user_same_address():
    setup_database(John(), Mary(), PPG())
    # create John's userlocation
    route = Routes.userlocations
    client.post(route, json={"phone":John().phone,"address":PPG().address})
    # then create Mary's
    data = {"phone":Mary().phone,"address":PPG().address}
    r = client.post(route, json=data)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["phone"] == Mary().phone
    assert r_json["address"] == PPG().address


"""
READ USER TESTS
"""

def test_get_user():
    setup_database(John())
    route = "{route}?phone={phone}".format(route=Routes.users, phone=John().phone)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["name"] == John().name
    assert r_json["phone"] == John().phone


def test_get_nonexistent_user():
    route = "{route}?phone={phone}".format(route=Routes.users, phone="000000000")
    r = client.get(route)
    assert r.status_code == 404


def test_get_user_no_phone():
    route = "{route}".format(route=Routes.users)
    r = client.get(route)
    assert r.status_code == 422


"""
READ LOCATION TESTS
"""

def test_get_location():
    setup_database(PPG())
    route = "{route}?address={address}".format(route=Routes.locations, address=PPG().address)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["address"] == PPG().address


def test_get_nonexistent_location():
    route = "{route}?address={address}".format(route=Routes.locations, address="not a real address")
    r = client.get(route)
    assert r.status_code == 404


def test_get_location_no_address():
    route = "{route}".format(route=Routes.locations)
    r = client.get(route)
    assert r.status_code == 422


"""
READ USERLOCATION TESTS
"""

def test_get_one_user_location():
    setup_database(John(), PPG())
    ul_nickname = "Work"
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address,"nickname":ul_nickname})
    route = "{route}?phone={phone}&nickname={nickname}".format(route=Routes.userlocations, phone=John().phone, nickname=ul_nickname)
    r = client.get(route)
    r_json = r.json()[0]
    assert r.status_code == 200
    assert r_json["phone"] == John().phone
    assert r_json["address"] == PPG().address
    assert r_json["nickname"] == ul_nickname


def test_get_all_user_locations():
    setup_database(John(), PPG(), Heinz())
    addresses = {PPG().address, Heinz().address}
    for address in addresses:
        client.post(Routes.userlocations, json={"phone":John().phone, "address":address})
    route = "{route}?phone={phone}".format(route=Routes.userlocations, phone=John().phone)
    r = client.get(route)
    assert r.status_code == 200
    r_json_list = r.json()
    for ul_json in r_json_list:
        assert ul_json["phone"] == John().phone
        assert ul_json["address"] in addresses
        addresses.remove(ul_json["address"])


def test_get_nonexistent_user_location():
    ul_nickname = "Work"
    route = "{route}?phone={phone}&nickname={nickname}".format(route=Routes.userlocations, phone=John().phone, nickname=ul_nickname)
    r = client.get(route)
    assert r.status_code == 404


def test_get_user_location_no_phone():
    setup_database(John(), PPG())
    ul_nickname = "Work"
    client.post(Routes.userlocations, json={"phone":John().phone, "address":PPG().address, "nickname":ul_nickname})
    route = "{route}?nickname={nickname}".format(route=Routes.userlocations, nickname=ul_nickname)
    r = client.get(route)
    assert r.status_code == 422


"""
DELETE USER TESTS
"""

def test_delete_user():
    setup_database(John())
    route = "{route}?phone={phone}".format(route=Routes.users, phone=John().phone)
    r = client.delete(route)
    assert r.status_code == 200


def test_delete_nonexistent_user():
    route = "{route}?phone={phone}".format(route=Routes.users, phone=John().phone)
    r = client.delete(route)
    assert r.status_code == 404


def test_delete_user_cascade_delete_user_locations():
    setup_database(John())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    # delete user
    route = "{route}?phone={phone}".format(route=Routes.users, phone=John().phone)
    r = client.delete(route)
    assert r.status_code == 200
    # check userlocation deletion
    route = "{route}?phone={phone}".format(route=Routes.userlocations, phone=John().phone)
    r = client.get(route)
    assert r.status_code == 404


"""
DELETE LOCATION TESTS
"""

def test_delete_location():
    setup_database(PPG())
    route = "{route}?address={address}".format(route=Routes.locations, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 200


def test_delete_nonexistent_location():
    route = "{route}?address={address}".format(route=Routes.locations, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 404


def test_delete_location_referenced_by_user_location():
    setup_database(John(), PPG())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    route = "{route}?address={address}".format(route=Routes.locations, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 409

"""
DELETE USER LOCATION TESTS
"""

def test_delete_user_location_by_nickname():
    setup_database(John(), PPG())
    ul_nickname = "Work"
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address,"nickname":ul_nickname})
    route = "{route}?phone={phone}&nickname={nickname}".format(route=Routes.userlocations, phone=John().phone, nickname=ul_nickname)
    r = client.delete(route)
    assert r.status_code == 200

def test_delete_user_location_by_address():
    setup_database(John(), PPG())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    route = "{route}?phone={phone}&address={address}".format(route=Routes.userlocations, phone=John().phone, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 200

def test_delete_user_location_no_phone():
    setup_database(John(), PPG())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    route = "{route}?address={address}".format(route=Routes.userlocations, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 422

def test_delete_user_location_only_phone():
    setup_database(John(), PPG())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    route = "{route}?phone={phone}".format(route=Routes.userlocations, phone=John().phone)
    r = client.delete(route)
    assert r.status_code == 422

def test_delete_nonexistent_user_location():
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    route = "{route}?phone={phone}&address={address}".format(route=Routes.userlocations, phone=John().phone, address=PPG().address)
    r = client.delete(route)
    assert r.status_code == 404

def test_delete_someone_elses_user_location():
    setup_database(John(), Mary(), PPG(), Heinz())
    client.post(Routes.userlocations, json={"phone":John().phone,"address":PPG().address})
    client.post(Routes.userlocations, json={"phone":Mary().phone,"address":Heinz().address})
    route = "{route}?phone={phone}&address={address}".format(route=Routes.userlocations, phone=John().phone, address=Heinz().address)
    r = client.delete(route)
    assert r.status_code == 404
