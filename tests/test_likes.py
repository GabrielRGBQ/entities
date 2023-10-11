import pytest
from app import models


@pytest.fixture()
def test_like(test_entities, session, test_user):
    new_like = models.Like(entity_id=test_entities[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_on_entity(authorized_client, test_entities):
    res = authorized_client.post(
        "/likes/", json={"entity_id": test_entities[3].id, "dir": 1})
    assert res.status_code == 201


def test_like_twice_entity(authorized_client, test_entities, test_like):
    res = authorized_client.post(
        "/likes/", json={"entity_id": test_entities[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_like(authorized_client, test_entities, test_like):
    res = authorized_client.post(
        "/likes/", json={"entity_id": test_entities[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_like_non_exist(authorized_client, test_entities):
    res = authorized_client.post(
        "/likes/", json={"entity_id": test_entities[3].id, "dir": 0})
    assert res.status_code == 404


def test_like_entity_non_exist(authorized_client, test_entities):
    res = authorized_client.post(
        "/likes/", json={"entity_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_like_unauthorized_user(client, test_entities):
    res = client.post(
        "/likes/", json={"entity_id": test_entities[3].id, "dir": 1})
    assert res.status_code == 401