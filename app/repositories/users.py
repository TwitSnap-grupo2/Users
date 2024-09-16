# from app.repositories.schemas import NewUser, User
from uuid import uuid4, UUID


from pydantic import EmailStr
from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def insert_user(db: Session, new_user: models.User) -> models.User:
    interests_list = [
        models.UserInterests(interest=schemas.Interests(interest))
        for interest in new_user.interests
    ]
    db_user = models.User(
        id=uuid4(),
        email=new_user.email,
        user=new_user.user,
        name=new_user.name,
        location=new_user.location,
        goals=[models.UsersGoals(goal=goal) for goal in new_user.goals],
        interests=interests_list,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email_or_name(db: Session, email: EmailStr, user: str) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.email == email or models.User.user == user)
        .first()
    )


def get_user_by_id(db: Session, user_id: UUID) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
