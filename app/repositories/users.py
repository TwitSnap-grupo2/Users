from app.repositories.models import NewUser, User
from uuid import uuid4, UUID

# Will change this soon
users_db: list[User] = []


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def get_users() -> list[User]:
    return users_db


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def insert_user(new_user: NewUser) -> User:
    user = User(**new_user.model_dump(), id=uuid4())

    users_db.append(user)

    return user


async def get_user(id: UUID) -> User | None:
    for user in users_db:
        if user.id == id:
            return user

    return None
