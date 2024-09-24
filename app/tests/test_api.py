from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.utils.schemas import NewUser, User, SignUpSchema
from app.tests import utils
import pytest

client = TestClient(app)

# Mock authentication token for tests
# auth_header = {"Authorization": "Bearer mock_token"}

# Sample user data for testing
test_user = NewUser(
    email="donpepo@test.com",
    user="Pepo",
    name="Don Pepo",
)

# Run before each test
@pytest.fixture(autouse=True)
def before_each():  
    # clear database
    utils.empty_database()

# Test getting users with an empty database
def test_get_users_with_empty_database_returns_an_empty_list():
    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

# Test getting users returns a list with the users
def test_get_users_returns_a_list_with_the_users():
    user: User = utils.create_user(test_user)
    dumped_user = user.model_dump()
    dumped_user["id"] = str(dumped_user["id"])

    # response = client.get("/users/", headers=auth_header)
    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [dumped_user]

# Test getting user by ID with no users returns not found error
def test_get_user_by_id_with_no_users_return_not_found_error():
    response = client.get(f"/users/{uuid4()}")
    response_json = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_json["type"]
    assert response_json["title"]
    assert response_json["status"] == status.HTTP_404_NOT_FOUND
    assert response_json["detail"]
    assert response_json["instance"]

# Test getting user by ID returns user if user exists
def test_get_user_by_id_returns_user_if_user_exists():
    user: User = utils.create_user(test_user)

    response = client.get(f"/users/{str(user.id)}")

    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert utils.contains_values(test_user.model_dump(), response_json)
    assert response_json["id"]

# Test signing up a new user
def test_post_signup_creates_user():
    test_user_with_password = SignUpSchema(**test_user.model_dump(), password="password")
    response = client.post(
        "/users/signup",
        json=test_user_with_password.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["email"] == test_user.email

# Test logging in with valid credentials
# def test_post_login_returns_access_token():
#     user: User = utils.create_user(test_user)
    
#     response = client.post(
#         "/users/login",
#         json={"email": test_user.email, "password": "valid_password"},  # Adjust this based on your implementation
#     )

#     assert response.status_code == status.HTTP_200_OK
#     assert "access_token" in response.json()

# Test setting user location
def test_set_location_updates_user_location():
    user: User = utils.create_user(test_user)
    
    response = client.post(
        f"/users/location/{user.id}",
        json={"location": "ARG"}  # Example location code
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["location"] == "ARG"

# Test setting user interests
def test_set_interests_updates_user_interests():
    user: User = utils.create_user(test_user)
    
    response = client.post(
        f"/users/interests/{user.id}",
        json=["science"],  # Example interest
    )

    assert response.status_code == status.HTTP_201_CREATED

# Test setting user goals
def test_set_goals_updates_user_goals():
    user: User = utils.create_user(test_user)
    
    response = client.post(
        f"/users/goals/{user.id}",
        json=["Learn FastAPI"],  # Example goal
    )

    assert response.status_code == status.HTTP_201_CREATED

