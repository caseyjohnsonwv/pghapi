import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, get_db
from src.database.database import Base
import env

#setup test db
engine = create_engine(
    env.TEST_DATABASE_URL, connect_args = {"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# automatically resets database between tests
@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# for adding records to database before each test
def setup_database(*objects):
    db = TestingSessionLocal()
    for obj in objects:
        db.add(obj)
        db.commit()


#point app to test db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

#create ref for tests to access app
client = TestClient(app)
