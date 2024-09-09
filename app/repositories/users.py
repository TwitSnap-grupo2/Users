from .models import NewUser, User, Interests


# Will change this soon
users_db: list[User] = [
    User(
        id="1",
        user="pepo",
        name="Don Pepo",
        location="Argentina",
        interests=["engineering"],
    ),
]


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def get_users() -> list[User]:
    return users_db


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def insert_user(new_user: NewUser) -> User:
    new_user_id = len(users_db) + 1

    new_user = User(**new_user.model_dump(), id=str(new_user_id))

    users_db.append(new_user)

    return new_user
