import uvicorn
from fastapi import FastAPI
import env
from src.database import models
from src.database.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

class Routes:
    healthcheck = '/healthcheck/'
    users = '/users/'
    locations = '/locations/'
    userlocations = '/user-locations/'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from src.routers import healthcheck, users, locations, userlocations
app = FastAPI()
app.include_router(healthcheck.router, prefix=Routes.healthcheck[:-1], tags=["healthcheck"])
app.include_router(users.router, prefix=Routes.users[:-1], tags=["users"])
app.include_router(locations.router, prefix=Routes.locations[:-1], tags=["locations"])
app.include_router(userlocations.router, prefix=Routes.userlocations[:-1], tags=["user-locations"])

if __name__ == "__main__":
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
