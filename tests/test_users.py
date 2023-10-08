from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

from app import schemas
from app.config import settings
from app.main import app
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Here is what is run before the test has been run
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Here is what is run after the test has been run
    # Base.metadata.drop_all(bind=engine)


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
