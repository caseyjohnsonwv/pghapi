import pytest
import env
from .startup import client

"""
TEST CASES BELOW
"""

def test_healthcheck():
    r = client.get('/healthcheck')
    assert r.status_code == 200
    assert r.json() == {"Status":"Alive"}
