from typing import List
from fastapi import APIRouter, HTTPException, Query
from src.database import schemas
from src.maps import gmapsworker
from .routes import Routes

router = APIRouter()

from main import get_db


@router.get(Routes.MapLookup.traveltime_suffix, response_model = schemas.TravelTime)
def read_traveltime(origin: str, destination: str):
    time_estimate = gmapsworker.get_travel_time(origin, destination)
    return {"origin":origin, "destination":destination, "time_estimate":time_estimate}
