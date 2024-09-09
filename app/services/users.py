# from app.repositories.users import get_users
from app.repositories.models import User
import app.repositories.users as db


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
async def fetch_users() -> list[User]:
    return await db.get_users()
