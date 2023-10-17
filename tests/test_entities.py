import pytest

from app import schemas


def test_get_all_entities(authorized_client, test_entities):
    res = authorized_client.get("/entities/")
    assert len(res.json()) == len(test_entities)
    assert res.status_code == 200


def test_unauthorized_user_get_all_entities(client):
    res = client.get("/entities/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_entity(client, test_entities):
    res = client.get(f"/entities/{test_entities[0].id}")
    assert res.status_code == 401


def test_get_one_entity_not_exist(authorized_client):
    res = authorized_client.get("/entities/88888")
    assert res.status_code == 404


def test_get_one_entity(authorized_client, test_entities):
    res = authorized_client.get(f"/entities/{test_entities[0].id}")
    entity = schemas.EntityOut(**res.json())
    assert entity.Entity.id == test_entities[0].id
    assert entity.Entity.description == test_entities[0].description
    assert entity.Entity.title == test_entities[0].title


@pytest.mark.parametrize(
    "title, description",
    [
        ("awesome new title", "awesome new content"),
        ("favorite pizza", "i love pepperoni"),
        ("tallest skyscrapers", "wahoo"),
    ],
)
def test_create_entity(authorized_client, test_user, title, description):
    res = authorized_client.post(
        "/entities/", json={"title": title, "description": description}
    )

    created_entity = schemas.Entity(**res.json())
    assert res.status_code == 201
    assert created_entity.title == title
    assert created_entity.description == description
    assert created_entity.owner_id == test_user["id"]


def test_unauthorized_user_create_entity(client):
    res = client.post(
        "/entities/", json={"title": "arbitrary title", "description": "aasdfjasdf"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_entity(client, test_entities):
    res = client.delete(f"/entities/{test_entities[0].id}")
    assert res.status_code == 401


def test_delete_entity_success(authorized_client, test_entities):
    res = authorized_client.delete(f"/entities/{test_entities[0].id}")

    assert res.status_code == 204


def test_delete_entity_non_exist(authorized_client):
    res = authorized_client.delete("/entities/8000000")

    assert res.status_code == 404


def test_delete_other_user_entity(authorized_client, test_entities):
    res = authorized_client.delete(f"/entities/{test_entities[3].id}")
    assert res.status_code == 403


def test_update_entity(authorized_client, test_entities):
    data = {
        "title": "updated title",
        "description": "updatd content",
        "id": test_entities[0].id,
    }
    res = authorized_client.put(f"/entities/{test_entities[0].id}", json=data)
    updated_entity = schemas.Entity(**res.json())
    assert res.status_code == 200
    assert updated_entity.title == data["title"]
    assert updated_entity.description == data["description"]


def test_update_other_user_entity(
    authorized_client, test_user, test_user2, test_entities
):
    data = {
        "title": "updated title",
        "description": "updatd content",
        "id": test_entities[3].id,
    }
    res = authorized_client.put(f"/entities/{test_entities[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_entity(client, test_user, test_entities):
    res = client.put(f"/entities/{test_entities[0].id}")
    assert res.status_code == 401


def test_update_entity_non_exist(authorized_client, test_user, test_entities):
    data = {
        "title": "updated title",
        "description": "updatd content",
        "id": test_entities[2].id,
    }
    res = authorized_client.put("/entities/8000000", json=data)

    assert res.status_code == 404
