from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.tests.utils import empty_database, contains_values, insert_user
import pytest


client = TestClient(app)


test_user = {
    "user": "Pepo",
    "name": "Don Pepo",
    "location": "Argentina",
    "interests": ["engineering"],
}


# Run before each test
@pytest.fixture(autouse=True)
def before_each():
    # clear database
    empty_database()


def test_get_users_with_empty_database_returns_an_empty_list():
    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_post_user_returns_created_user():
    response = client.post(
        "/users/",
        json=test_user,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert contains_values(test_user, response.json())
    assert response.json()["id"]


def test_get_users_returns_a_list_with_the_users():
    user = test_user
    user["id"] = "1"
    insert_user(user)

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [user]


def test_post_user_with_invalid_parameters_returns_error():
    user = test_user
    user["name"] = 1  # It's not a string, so the client will get an error

    response = client.post("/users/", json=user)
    response_json = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["type"]
    assert response_json["title"]
    assert response_json["status"] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"]
    assert response_json["instance"]
