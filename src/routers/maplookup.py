from typing import List
from fastapi import APIRouter, HTTPException, Query
from src.database import schemas
from .routes import Routes

router = APIRouter()

from main import get_db

# sanity-check method, ensures addresses are real
@router.get(Routes.MapLookup.address_suffix, response_model = schemas.Location)
def read_address(address: str):
    pass

@router.get(Routes.MapLookup.traveltime_suffix, response_model = schemas.TravelTime)
def read_traveltime(addresses: List[str] = Query(None)):
    pass
