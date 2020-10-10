from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, get_db
from src.database import Base
import env

client = None

def startup():
    #setup test db
    engine = create_engine(
        env.TEST_DATABASE_URL, connect_args = {"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    #drain db and recreate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    #point app to test db
    def override_get_db():
        try:
            db = TestingSessingLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db

    #create ref for tests to access app
    global client
    client = TestClient(app)
