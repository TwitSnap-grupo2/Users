from .models import User, Interests


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
async def get_users():
    return users_db
