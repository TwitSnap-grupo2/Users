from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.schemas import NewUser, User
from app.tests import utils
import pytest

client = TestClient(app)


test_user = NewUser(
    email="donpepo@test.com",
    user="Pepo",
    name="Don Pepo",
    location="Argentina",
    interests=["engineering"],
    goals=["Matear los domingos"],
)


# Run before each test
@pytest.fixture(autouse=True)
def before_each():
    # clear database
    utils.empty_database()


def test_get_users_with_empty_database_returns_an_empty_list():
    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_post_user_returns_created_user():
    response = client.post(
        "/users/",
        json=test_user.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert utils.contains_values(test_user.model_dump(), response.json())
    assert response.json()["id"]


def test_get_users_returns_a_list_with_the_users():
    user: User = utils.create_user(test_user)
    dumped_user = user.model_dump()
    dumped_user["id"] = str(dumped_user["id"])

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [dumped_user]


def test_post_user_with_invalid_parameters_returns_error():
    user = NewUser(**test_user.model_dump())
    user_dict = user.model_dump()
    user_dict["user"] = 1  # It's not a string, so the client will get an error

    response = client.post("/users/", json=user_dict)
    response_json = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["type"]
    assert response_json["title"]
    assert response_json["status"] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"]
    assert response_json["instance"]


def test_get_user_by_id_with_no_users_return_not_found_error():
    response = client.get(f"/users/{uuid4()}")
    response_json = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_json["type"]
    assert response_json["title"]
    assert response_json["status"] == status.HTTP_404_NOT_FOUND
    assert response_json["detail"]
    assert response_json["instance"]


def test_get_user_by_id_returns_user_if_user_exists():
    user: User = utils.create_user(test_user)

    response = client.get(f"/users/{str(user.id)}")

    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert utils.contains_values(test_user.model_dump(), response_json)
    assert response_json["id"]


def test_get_user_by_id_with_invalid_id_format_returns_error():
    response = client.get(f"/users/1")
    response_json = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["type"]
    assert response_json["title"]
    assert response_json["status"] == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_json["detail"]
    assert response_json["instance"]
