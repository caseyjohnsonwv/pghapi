import pytest
import env
from .startup import client

"""
TEST CASES BELOW
"""

def test_healthcheck():
    route = "/healthcheck"
    r = client.get(route)
    assert r.status_code == 200
    assert r.json() == {"Status":"Alive"}
