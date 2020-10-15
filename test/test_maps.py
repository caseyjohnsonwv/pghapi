import pytest
import env
from src.database import models
from .startup import client, setup_database, reset_database
from .dummy_data import *
from src.routers.routes import Routes


"""
TRAVELTIME TESTS
"""

def test_query_traveltime_with_googlemaps():
    address1 = PPG().address
    address2 = Steelers().address
    route = "{route}?origin={origin}&destination={destination}".format(route=Routes.MapLookup.traveltime, origin=address1, destination=address2)
    r = client.get(route)
    r_json = r.json()
    assert r.status_code == 200
    assert r_json["origin"] == address1
    assert r_json["destination"] == address2
    assert r_json["time_estimate"] is not None
