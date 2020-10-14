import uvicorn
from fastapi import FastAPI
import env
from src.database import models
from src.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# cannot import sooner due to circular ref with get_db
from src.routers import healthcheck, users, locations, userlocations, maplookup
from src.routers.routes import Routes

app = FastAPI()
app.include_router(healthcheck.router, prefix=Routes.healthcheck_prefix, tags=["healthcheck"])
app.include_router(users.router, prefix=Routes.users_prefix, tags=["users"])
app.include_router(locations.router, prefix=Routes.locations_prefix, tags=["locations"])
app.include_router(userlocations.router, prefix=Routes.userlocations_prefix, tags=["user-locations"])
app.include_router(maplookup.router, prefix=Routes.maplookup_prefix, tags=["maplookup"])

if __name__ == "__main__":
    uvicorn.run(app, host=env.HOST_ADDRESS, port=env.HOST_PORT)
