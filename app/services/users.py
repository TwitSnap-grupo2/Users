# from app.repositories.users import get_users
from sqlalchemy.orm import Session

from app.repositories import users, models, schemas
from app.repositories.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


class ExistentUserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def __database_model_to_schema(user: schemas.DatabaseUser) -> schemas.User:

    return schemas.User(
        id=user.id,
        email=user.email,
        user=user.user,
        name=user.name,
        location=user.location,
        goals=[g.goal for g in user.goals],
        interests=[interest.interest for interest in user.interests],
        twitsnaps=[twitsnap.id_twitsnap for twitsnap in user.twitsnaps],
        followers=[follower.follower_id for follower in user.followers],
    )


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
def fetch_users(db: Session) -> list[schemas.User]:
    db_users: list[schemas.DatabaseUser] = users.get_users(db)

    return [__database_model_to_schema(user) for user in db_users]


def create_user(db: Session, new_user: schemas.NewUser) -> schemas.User:
    user = users.get_user_by_email_or_name(
        db=db, email=new_user.email, user=new_user.user
    )
    if not user:
        db_user = users.insert_user(db=db, new_user=new_user)
        return __database_model_to_schema(db_user)

    # If here, then the user exists, so check for email or user repetition
    if user.email == new_user.email:
        raise ExistentUserError("Mail is already registered")
    if user.user == new_user.user:
        raise ExistentUserError("Username is already registered")


# async def create_user(new_user: NewUser) -> User:
#     return await db.insert_user(new_user)


# async def fetch_user(id: UUID) -> User | None:
#     return await db.get_user(id)
