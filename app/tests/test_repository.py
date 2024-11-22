import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from app.repositories import models
from app.repositories.users import (
    get_followeds,
    get_followers,
    get_recommendations,
    get_users,
    insert_user,
    get_user_by_email_or_name,
    get_user_by_email,
    get_user_by_id,
    empty_users,
    modify_block_status,
    set_location,
    set_interests,
    set_goals,
    add_follower,
    remove_follow,
)
from app.tests.utils import generate_user
from app.utils import schemas
from app.utils.errors import NotAllowed, UserNotFound


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.user: models.User = generate_user(
            email="test@example.com",
            user="test_user",
            name="Test User",
            location="ARG",
        )
        self.user2: models.User = generate_user(
            email="test2@example.com",
            user="test_user2",
            name="Test User 2",
            location="ARG",
        )

    def test_get_users(self):
        self.db_mock.query.return_value.all.return_value = [self.user]
        users = get_users(self.db_mock)
        self.assertEqual(users, [self.user])

    def test_insert_user(self):
        new_user = schemas.NewUser(
            email="new@example.com", user="new_user", name="New User", location="ARG"
        )
        self.db_mock.add = MagicMock()
        self.db_mock.commit = MagicMock()
        self.db_mock.refresh = MagicMock()

        result_user = insert_user(self.db_mock, new_user)

        self.assertIsInstance(result_user, models.User)
        self.db_mock.add.assert_called_once()
        self.db_mock.commit.assert_called_once()

    def test_get_user_by_email_or_name(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        result_user = get_user_by_email_or_name(
            self.db_mock, self.user.email, "test_user"
        )
        self.assertEqual(result_user, self.user)

    def test_get_user_by_email(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        result_user = get_user_by_email(self.db_mock, self.user.email)
        self.assertEqual(result_user, self.user)

    def test_get_user_by_id(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        result_user = get_user_by_id(self.db_mock, self.user.id)
        self.assertEqual(result_user, self.user)

    def test_empty_users(self):
        self.db_mock.query.return_value.delete = MagicMock()
        empty_users(self.db_mock)
        self.db_mock.query.return_value.delete.assert_called()
        self.db_mock.commit.assert_called_once()

    def test_set_location(self):
        self.user.location = ""
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        location = "ARG"
        updated_user = set_location(self.db_mock, self.user.id, location=location)
        self.assertEqual(updated_user.location, location)

    def test_set_interests(self):
        self.user.interests = []
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        interests = [
            models.UserInterests(interest="science"),
            models.UserInterests(interest="engineering"),
        ]
        updated_user = set_interests(self.db_mock, self.user.id, interests)
        self.assertEqual(updated_user.interests, interests)
        self.db_mock.commit.assert_called_once()

    def test_set_goals(self):
        self.user.goals = []
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        goals = [models.UsersGoals(goal="Become a better developer")]
        updated_user = set_goals(self.db_mock, self.user.id, goals)
        self.assertEqual(updated_user.goals, goals)
        self.db_mock.commit.assert_called_once()

    def test_add_follower(self):
        # Simulate `get_user_by_id` returning two users: the follower and the followed
        self.db_mock.query.return_value.filter.return_value.first.side_effect = [
            self.user,  # source user (follower)
            self.user2,  # followed user
        ]
        # Initially the source user is not following the followed user
        self.user.followeds = []
        self.user2.followers = []

        updated_user = add_follower(self.db_mock, self.user.id, self.user2.id)

        self.assertIn(self.user, self.user2.followers)
        self.assertIn(self.user2, self.user.followeds)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_any_call(self.user)
        self.db_mock.refresh.assert_any_call(self.user2)

    def test_add_follower_already_following(self):
        # Simulate `get_user_by_id` returning two users: the follower and the followed
        self.db_mock.query.return_value.filter.return_value.first.side_effect = [
            self.user,  # source user (follower)
            self.user2,  # followed user
        ]

        self.user.followeds = [self.user2]
        self.user2.followers = [self.user]

        with self.assertRaises(NotAllowed):
            add_follower(self.db_mock, self.user.id, self.user2.id)

    def test_remove_follow(self):
        # Simulate `get_user_by_id` returning two users: the follower and the followed
        self.db_mock.query.return_value.filter.return_value.first.side_effect = [
            self.user,  # source user (follower)
            self.user2,  # followed user
        ]

        self.user.followeds = [self.user2]
        self.user2.followers = [self.user]

        updated_user = remove_follow(self.db_mock, self.user.id, self.user2.id)

        self.assertNotIn(self.user, self.user2.followers)
        self.assertNotIn(self.user2, self.user.followeds)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_any_call(self.user)
        self.db_mock.refresh.assert_any_call(self.user2)

    def test_remove_follow_not_following(self):
        # Simulate `get_user_by_id` returning two users: the follower and the followed
        self.db_mock.query.return_value.filter.return_value.first.side_effect = [
            self.user,  # source user (follower)
            self.user2,  # followed user
        ]

        self.user.followeds = []
        self.user2.followers = []

        with self.assertRaises(NotAllowed):
            remove_follow(self.db_mock, self.user.id, self.user2.id)

    def test_get_followers(self):
        self.user.followers = [self.user2]
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        followers = get_followers(self.db_mock, self.user.id)

        self.assertEqual(followers, self.user.followers)
        self.db_mock.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_followers_user_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(UserNotFound) as context:
            get_followers(self.db_mock, self.user.id)

        self.assertEqual(str(context.exception), "No user was found for the given id")

    def test_get_followeds(self):
        self.user.followeds = [self.user2]
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        followeds = get_followeds(self.db_mock, self.user.id)

        self.assertEqual(followeds, self.user.followeds)
        self.db_mock.query.return_value.filter.return_value.first.assert_called_once()

    def test_get_followeds_user_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(UserNotFound) as context:
            get_followeds(self.db_mock, self.user.id)

        self.assertEqual(str(context.exception), "No user was found for the given id")

    def test_get_recommendations_success(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        self.db_mock.execute.return_value.mappings.return_value = [
            {
                "id": str(uuid4()),
                "name": "Recommended User 1",
                "user": "recommended_user1",
            },
            {
                "id": str(uuid4()),
                "name": "Recommended User 2",
                "user": "recommended_user2",
            },
        ]

        recommendations = get_recommendations(self.db_mock, self.user.id)

        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]["name"], "Recommended User 1")
        self.assertEqual(recommendations[1]["name"], "Recommended User 2")

    def test_get_recommendations_no_results(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        self.db_mock.execute.return_value.mappings.return_value = []

        recommendations = get_recommendations(self.db_mock, self.user.id)

        self.assertEqual(len(recommendations), 0)

    def test_get_recommendations_location_based(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        self.db_mock.execute.return_value.mappings.return_value = [
            {"id": str(uuid4()), "name": "Nearby User", "user": "nearby_user"}
        ]

        recommendations = get_recommendations(self.db_mock, self.user.id)

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["name"], "Nearby User")
        self.assertEqual(recommendations[0]["user"], "nearby_user")

    def test_get_recommendations_interest_based(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        self.db_mock.execute.return_value.mappings.return_value = [
            {"id": str(uuid4()), "name": "Interest-Based User", "user": "interest_user"}
        ]

        recommendations = get_recommendations(self.db_mock, self.user.id)

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]["name"], "Interest-Based User")
        self.assertEqual(recommendations[0]["user"], "interest_user")

    def test_get_recommendations_user_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(UserNotFound) as context:
            get_recommendations(self.db_mock, self.user.id)

        self.assertEqual(str(context.exception), "No user was found for the given id")

    def test_block_user_not_foiund(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(UserNotFound) as context:
            modify_block_status(self.db_mock, self.user.id, block_status=True)

        self.assertEqual(str(context.exception), "No user was found for the given id")

    def test_unblock_user_not_foiund(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaises(UserNotFound) as context:
            modify_block_status(self.db_mock, self.user.id, block_status=False)

        self.assertEqual(str(context.exception), "No user was found for the given id")

    def test_block_user(self):
        self.user.is_blocked = False
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        updated_user = modify_block_status(
            self.db_mock, self.user.id, block_status=True
        )
        self.assertNotEqual(updated_user.is_blocked, updated_user)

    def test_unblock_user(self):
        self.user.is_blocked = True
        self.db_mock.query.return_value.filter.return_value.first.return_value = (
            self.user
        )
        updated_user = modify_block_status(
            self.db_mock, self.user.id, block_status=False
        )
        self.assertNotEqual(updated_user.is_blocked, updated_user)


if __name__ == "__main__":
    unittest.main()
