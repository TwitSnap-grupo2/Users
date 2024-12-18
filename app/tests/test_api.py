from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient
from app.services.users import follow
from app.main import app
from app.utils.schemas import (
    Admin,
    SignUpAdminSchema,
    User,
    SignUpSchema,
    Interests,
    UserWithoutId,
)
from app.tests import utils
import pytest

client = TestClient(app)

test_user = SignUpSchema(
    email="donpepo@test.com",
    password="pepo",
    user="Pepo",
    name="Don Pepo",
    location="ARG",
)

test_admin = SignUpAdminSchema(
    email="donpepo@admin.com",
    password="pepo",
    user="pepiAdmin",
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
    response_user = test_user.model_dump()
    del response_user["password"]

    response = client.get(f"/users/{str(user.id)}")

    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert utils.contains_values(response_user, response_json)
    assert response_json["id"]


# Test signing up a new user
def test_post_signup_creates_user():
    response = client.post(
        "/users/signup",
        json=test_user.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["email"] == test_user.email


# Test setting user location
def test_set_location_updates_user_location():
    user: User = utils.create_user(test_user)

    response = client.post(
        f"/users/location/{user.id}", json={"location": "ARG"}  # Example location code
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


def test_add_follower_updates_user_followers():
    user: User = utils.create_user(test_user)
    follower_user_data = SignUpSchema(
        email="follower@test.com",
        password="followerpass",
        user="Follower",
        name="Follower User",
        location="ARG",
    )
    follower: User = utils.create_user(follower_user_data)

    response = client.post(
        f"/users/follow/{follower.id}",
        json=str(user.id),
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert "id" in response_json
    assert response_json["user"] == follower.user
    assert len(response_json["followeds"]) == 1
    assert response_json["followeds"][0] == str(user.id)


def test_add_follower_already_following():
    user: User = utils.create_user(test_user)
    follower_user_data = SignUpSchema(
        email="follower@test.com",
        password="followerpass",
        user="Follower",
        name="Follower User",
        location="ARG",
    )
    follower: User = utils.create_user(follower_user_data)

    # First follow
    client.post(f"/users/follow/{follower.id}", json=str(user.id))

    # Second attempt to follow the same user
    response = client.post(f"/users/follow/{follower.id}", json=str(user.id))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_json = response.json()
    assert response_json["detail"] == f"The user is already following {user.name}"


def test_remove_follower():
    user: User = utils.create_user(test_user)
    follower_user_data = SignUpSchema(
        email="follower@test.com",
        password="followerpass",
        user="Follower",
        name="Follower User",
        location="ARG",
    )
    follower: User = utils.create_user(follower_user_data)

    # Follow user first
    client.post(f"/users/follow/{follower.id}", json=str(user.id))

    # Now remove the follow
    response = client.delete(
        f"/users/follow/{follower.id}",
        params={"followed_id": str(user.id)},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == str(follower.id)
    assert len(response_json["followeds"]) == 0


def test_remove_follower_not_following():
    user: User = utils.create_user(test_user)
    follower_user_data = SignUpSchema(
        email="follower@test.com",
        password="followerpass",
        user="Follower",
        name="Follower User",
        location="ARG",
    )
    follower: User = utils.create_user(follower_user_data)

    # Attempt to unfollow without following first
    response = client.delete(
        f"/users/follow/{follower.id}",
        params={"followed_id": str(user.id)},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_json = response.json()
    assert response_json["detail"] == f"Cannot unfollow an unfollowed user: {user.name}"


# Test getting followers of a user with no followers
def test_get_followers_with_no_followers():
    user: User = utils.create_user(test_user)

    response = client.get(f"/users/followers/{str(user.id)}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


# Test getting followeds of a user with no followeds
def test_get_followeds_with_no_followeds():
    user: User = utils.create_user(test_user)

    response = client.get(f"/users/followeds/{str(user.id)}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


# Test getting followers of a user with followers
def test_get_followers_with_followers():
    user: User = utils.create_user(test_user)
    follower_user_data = SignUpSchema(
        email="follower@test.com",
        password="followerpass",
        user="Follower",
        name="Follower User",
        location="ARG",
    )
    follower: User = utils.create_user(follower_user_data)

    # First, the follower follows the user
    client.post(f"/users/follow/{follower.id}", json=str(user.id))

    # Now get followers of the user
    response = client.get(f"/users/followers/{str(user.id)}")

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["id"] == str(follower.id)
    assert response_json[0]["user"] == follower.user


# Test getting followeds of a user with followeds
def test_get_followeds_with_followeds():
    user: User = utils.create_user(test_user)
    followed_user_data = SignUpSchema(
        email="followed@test.com",
        password="followedpass",
        user="Followed",
        name="Followed User",
        location="ARG",
    )
    followed: User = utils.create_user(followed_user_data)

    # First, the user follows the followed user
    client.post(f"/users/follow/{user.id}", json=str(followed.id))

    # Now get followeds of the user
    response = client.get(f"/users/followeds/{str(user.id)}")

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["id"] == str(followed.id)
    assert response_json[0]["user"] == followed.user


# Test getting followers of a non-existent user
def test_get_followers_of_non_existent_user():
    response = client.get(f"/users/followers/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json["detail"] == "No user was found for the given id"


# Test getting followeds of a non-existent user
def test_get_followeds_of_non_existent_user():
    response = client.get(f"/users/followeds/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json["detail"] == "No user was found for the given id"


def test_post_admin_signup_creates_admin():
    response = client.post(
        "/users/admin/signup",
        json=test_admin.model_dump(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["email"] == test_admin.email


def test_update_users_name_of_non_existent_user():
    response = client.put(
        f"/users/name/{uuid4()}?name=NewName",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json["detail"] == "No user was found for the given id"


def test_update_users_name():
    user: User = utils.create_user(test_user)
    response = client.put(
        f"/users/name/{str(user.id)}?name=NewName",
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["name"] == "NewName"
    assert response_json["id"] == str(user.id)
    assert response_json["user"] == user.user
    assert response_json["email"] == user.email
    assert response_json["location"] == user.location
    assert response_json["goals"] == user.goals
    assert response_json["interests"] == user.interests
    assert response_json["followers"] == user.followers
    assert response_json["followeds"] == user.followeds
    assert response_json["twitsnaps"] == user.twitsnaps


def test_get_interests():
    response = client.get("/users/interests/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [interest for interest in Interests]


def test_search_users_returns_users_ordered_by_similarity():
    user1: User = utils.create_user(
        SignUpSchema(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
        )
    )
    user2: User = utils.create_user(
        SignUpSchema(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ARG",
        )
    )
    user3: User = utils.create_user(
        SignUpSchema(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="ARG",
        )
    )
    user4: User = utils.create_user(
        SignUpSchema(
            email="user4@gmail.com",
            password="user4pass",
            user="imnotsimilar",
            name="user4",
            location="ARG",
        )
    )
    user5: User = utils.create_user(
        SignUpSchema(
            email="user5@gmail.com",
            password="user5pass",
            user="imausertoo",
            name="user5",
            location="ARG",
        )
    )

    response = client.get("/users/search?user=therealuser&limit=10")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert len(response_json) == 3
    assert response_json[0]["id"] == str(user1.id)
    assert response_json[1]["id"] == str(user3.id)
    assert response_json[2]["id"] == str(user2.id)


def test_search_followeds_returns_followeds_ordered_by_similarity():
    user1: User = utils.create_user(
        SignUpSchema(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
        )
    )
    user2: User = utils.create_user(
        SignUpSchema(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ARG",
        )
    )
    user3: User = utils.create_user(
        SignUpSchema(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="ARG",
        )
    )
    user4: User = utils.create_user(
        SignUpSchema(
            email="user4@gmail.com",
            password="user4pass",
            user="therealuser566",
            name="user4",
            location="ARG",
        )
    )

    client.post(f"/users/follow/{user1.id}", json=str(user2.id))
    client.post(f"/users/follow/{user1.id}", json=str(user3.id))

    response = client.get(
        f"/users/followeds/{user1.id}/search?user=therealuser&limit=10"
    )
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert len(response_json) == 2
    assert response_json[0]["id"] == str(user3.id)
    assert response_json[1]["id"] == str(user2.id)


def test_recommendations_with_no_coincidences_returns_an_empty_array():
    user1: User = utils.create_user(
        SignUpSchema(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
        )
    )

    res = client.get(f"/users/recommendations/{user1.id}")

    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert len(res_json) == 0


def test_recommendations_with_location_coincidences():
    user1: User = utils.create_user(
        SignUpSchema(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
        )
    )
    user2: User = utils.create_user(
        SignUpSchema(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="USA",
        )
    )
    user3: User = utils.create_user(
        SignUpSchema(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ARG",
        )
    )

    res = client.get(f"/users/recommendations/{user1.id}")

    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert len(res_json) == 1
    assert res_json[0]["id"] == str(user3.id)
    assert res_json[0]["name"] == user3.name
    assert res_json[0]["user"] == user3.user


def test_recommendations_with_interest_coincidences():
    user1: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
            interests=[Interests("engineering")],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user2: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="USA",
            interests=[Interests("engineering")],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user3: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ARG",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )

    res = client.get(f"/users/recommendations/{user1.id}")

    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert len(res_json) == 2


def test_recommendations_with_followeds_followeds():
    user1: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user2: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="USA",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user3: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ATG",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )

    utils.follow(user3.id, user2.id)
    utils.follow(user2.id, user1.id)

    res = client.get(f"/users/recommendations/{user3.id}")

    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert len(res_json) == 1
    assert res_json[0]["id"] == str(user1.id)
    assert res_json[0]["user"] == user1.user
    assert res_json[0]["name"] == user1.name


def test_recommendations_with_followeds_followeds_does_not_include_an_already_followed_user():
    user1: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user1@gmail.com",
            password="user1pass",
            user="therealuser",
            name="user1",
            location="ARG",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user2: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user2@gmail.com",
            password="user2pass",
            user="therealuser2",
            name="user2",
            location="USA",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )
    user3: User = utils.create_user_with_all_fields(
        UserWithoutId(
            email="user3@gmail.com",
            password="user3pass",
            user="realuser3",
            name="user3",
            location="ATG",
            interests=[],
            goals=[],
            followeds=[],
            followers=[],
            twitsnaps=[],
        )
    )

    utils.follow(user3.id, user1.id)
    utils.follow(user3.id, user2.id)
    utils.follow(user2.id, user1.id)

    res = client.get(f"/users/recommendations/{user3.id}")

    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()

    assert len(res_json) == 0


def test_block_non_existent_user():
    response = client.patch(
        f"/users/block/{uuid4()}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json["detail"] == "No user was found for the given id"


def test_unblock_non_existent_user():
    response = client.patch(
        f"/users/unblock/{uuid4()}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_json = response.json()
    assert response_json["detail"] == "No user was found for the given id"


def test_block_user():
    user: User = utils.create_user(test_user)

    response = client.patch(
        f"/users/block/{user.id}",
    )
    response_user = user.model_dump()
    response_user["is_blocked"] = True
    response_user["id"] = str(response_user["id"])

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert utils.contains_values(response_user, response_json)


def test_get_user_by_id_when_blocked():
    user: User = utils.create_user(test_user)

    client.patch(
        f"/users/block/{user.id}",
    )
    response = client.get(
        f"/users/{user.id}",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_json = response.json()
    assert response_json["detail"] == "This user is currently blocked"


def test_get_user_by_email_when_blocked():
    user: User = utils.create_user(test_user)

    client.patch(
        f"/users/block/{user.id}",
    )
    response = client.get(
        f"/users/email/{user.email}",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_json = response.json()
    assert response_json["detail"] == "This user is currently blocked"


def test_unblock_blocked_user():
    user: User = utils.create_user(test_user)

    client.patch(
        f"/users/block/{user.id}",
    )
    response = client.patch(
        f"/users/unblock/{user.id}",
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == str(user.id)
    assert response_json["is_blocked"] == False
