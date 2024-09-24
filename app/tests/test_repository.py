import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from app.repositories import models
from app.repositories.users import (
    get_users,
    insert_user,
    get_user_by_email_or_name,
    get_user_by_email,
    get_user_by_id,
    empty_users,
    set_location,
    set_interests,
    set_goals
)
from app.utils import schemas


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.user_id = uuid4()
        self.email = "test@example.com" 
        self.user = models.User(
            id=self.user_id,
            email=self.email,
            user="test_user",
            name="Test User",
            location="",
            goals=[],
            interests=[],
            followers=[],
            twitsnaps=[]
        )

    def test_get_users(self):
        self.db_mock.query.return_value.all.return_value = [self.user]
        users = get_users(self.db_mock)
        self.assertEqual(users, [self.user])

    def test_insert_user(self):
        new_user = schemas.NewUser(
            email="new@example.com",
            user="new_user",
            name="New User"
        )
        self.db_mock.add = MagicMock()
        self.db_mock.commit = MagicMock()
        self.db_mock.refresh = MagicMock()
        
        result_user = insert_user(self.db_mock, new_user)
        
        self.assertIsInstance(result_user, models.User)
        self.db_mock.add.assert_called_once()
        self.db_mock.commit.assert_called_once()

    def test_get_user_by_email_or_name(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        result_user = get_user_by_email_or_name(self.db_mock, self.email, "test_user")
        self.assertEqual(result_user, self.user)

    def test_get_user_by_email(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        result_user = get_user_by_email(self.db_mock, self.email)
        self.assertEqual(result_user, self.user)

    def test_get_user_by_id(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        result_user = get_user_by_id(self.db_mock, self.user_id)
        self.assertEqual(result_user, self.user)

    def test_empty_users(self):
        self.db_mock.query.return_value.delete = MagicMock()
        empty_users(self.db_mock)
        self.db_mock.query.return_value.delete.assert_called_once()
        self.db_mock.commit.assert_called_once()

    def test_set_location(self):
        self.user.location = ""
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        location = "ARG"
        updated_user = set_location(self.db_mock, self.user_id, location=location)
        self.assertEqual(updated_user.location, location)

    def test_set_interests(self):
        self.user.interests = []
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        interests = [models.UserInterests(interest="science"), models.UserInterests(interest="engineering")]
        updated_user = set_interests(self.db_mock, self.user_id, interests)
        self.assertEqual(updated_user.interests, interests)
        self.db_mock.commit.assert_called_once()

    def test_set_goals(self):
        self.user.goals = []
        self.db_mock.query.return_value.filter.return_value.first.return_value = self.user
        goals = [models.UsersGoals(goal="Become a better developer")]
        updated_user = set_goals(self.db_mock, self.user_id, goals)
        self.assertEqual(updated_user.goals, goals)
        self.db_mock.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
