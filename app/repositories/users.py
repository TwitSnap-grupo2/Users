# from app.repositories.schemas import NewUser, User
from uuid import uuid4, UUID

# # Will change this soon
# users_db: list[User] = []


# # Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
# async def get_users() -> list[User]:
# return users_db


# # Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
# async def insert_user(new_user: NewUser) -> User:
#     user = User(**new_user.model_dump(), id=uuid4())

#     users_db.append(user)

#     return user


# async def get_user(id: UUID) -> User | None:
#     for user in users_db:
#         if user.id == id:
#             return user

#     return None


from sqlalchemy.orm import Session

from . import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()

    # return db.query(models.User).offset(skip).limit(limit).all()


def insert_user(db: Session, new_user: models.User):
    interests_list = [schemas.Interests(interest) for interest in new_user.interests]

    db_user = models.User(
        id=uuid4(),
        email=new_user.email,
        user=new_user.user,
        name=new_user.name,
        location=new_user.location,
        goals=[models.UsersGoals(goal=goal) for goal in new_user.goals],
        interests=[
            models.UserInterests(interest=interest) for interest in interests_list
        ],
    )

    # db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
