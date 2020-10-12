from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_healthcheck():
    return {"Status":"Alive"}
