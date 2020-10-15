from typing import List
from datetime import datetime
import googlemaps
import env
from src.database import schemas

gmaps = googlemaps.Client(key=env.GOOGLE_MAPS_API_KEY)

"""
With "n" origin/destination pairs, the i'th estimate is:

r['rows'][i]['elements'][i]['duration']['text'].

This is because the DistanceMatrix API queries every combination of origin and destination.
Rows contain unique origins, elements contain unique destinations.

ie, the response is a table and its diagonal has unique combinations of origins/destinations.
"""


def standardize_address(address: str):
    pass


# for now, assume only one origin and destination
def get_travel_time(origin: str, destination: str):
    r = gmaps.distance_matrix(origins=origin, destinations=destination)
    return r['rows'][0]['elements'][0]['duration']['text']
