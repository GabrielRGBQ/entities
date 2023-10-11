import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app import models
from app.main import app
from app.oauth2 import create_access_token

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


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_entities(test_user, test_user2, session):
    entities_data = [
        {
            "title": "Entity 1",
            "description": "Description of entity 1",
            "owner_id": test_user["id"],
        },
        {
            "title": "Entity 2",
            "description": "Description of entity 2",
            "owner_id": test_user["id"],
        },
        {
            "title": "Entity 3",
            "description": "Description of entity 3",
            "owner_id": test_user["id"],
        },
        {
            "title": "Entity 4",
            "description": "Description of entity 4",
            "owner_id": test_user2["id"],
        }
    ]

    def create_entity_model(entity):
        return models.Entity(**entity)

    entity_map = map(create_entity_model, entities_data)
    entities = list(entity_map)

    session.add_all(entities)
    session.commit()

    entities = session.query(models.Entity).all()
    return entities
