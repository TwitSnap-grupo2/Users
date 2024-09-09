# from app.repositories.users import get_users
from app.repositories.models import NewUser, User
import app.repositories.users as db


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def fetch_users() -> list[User]:
    return await db.get_users()


async def create_user(new_user: NewUser) -> User:
    return await db.insert_user(new_user)
