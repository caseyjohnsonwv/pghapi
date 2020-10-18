from src.database import models


"""
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
    return models.Location(address="1 PPG Pl, Pittsburgh, PA 15222, USA")
def Heinz():
    return models.Location(address="300 Heinz St, Pittsburgh, PA 15212, USA")
def Steelers():
    return models.Location(address="100 Art Rooney Ave, Pittsburgh, PA 15212, USA")
