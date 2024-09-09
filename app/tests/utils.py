from app.repositories.models import User
from app.repositories.users import users_db


def empty_database():
    # TODO: change this for a testing db when database is implemented
    users_db.clear()


def contains_values(expected_values, response_dict):
    return all(item in response_dict.items() for item in expected_values.items())


def insert_user(user: User):
    users_db.append(user)
