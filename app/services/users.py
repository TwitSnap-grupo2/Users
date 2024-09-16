# from app.repositories.users import get_users
from uuid import UUID
from app.repositories.schemas import Interests, NewUser, User
import app.repositories.users as db

from sqlalchemy.orm import Session

from app.repositories import users, models
from app.repositories.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
def fetch_users(db: Session) -> list[User]:
    db_users: list[models.User] = users.get_users(db)
    return db_users


def create_user(db: Session, new_user: NewUser):
    # TODO: Check if it exists

    return users.insert_user(db=db, new_user=new_user)


# async def create_user(new_user: NewUser) -> User:
#     return await db.insert_user(new_user)


# async def fetch_user(id: UUID) -> User | None:
#     return await db.get_user(id)
