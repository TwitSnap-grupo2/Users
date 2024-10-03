import os
from uuid import uuid4

from pydantic import EmailStr
from app.repositories import models, users, database
from app.services import users as users_service
from app.utils import schemas


def empty_database():
    db = next(database.get_db())
    users.empty_users(db=db)


def create_user(new_user: schemas.SignUpSchema) -> schemas.User:
    db = next(database.get_db())
    return users_service.signup(db=db, new_user=new_user)


def contains_values(expected_values, response_dict) -> bool:
    return all(item in response_dict.items() for item in expected_values.items())


def generate_user(email: EmailStr, user: str, name: str) -> models.User:
    return models.User(
        id=uuid4(),
        email=email,
        user=user,
        name=name,
        location="",
        goals=[],
        interests=[],
        followers=[],
        twitsnaps=[],
    )
