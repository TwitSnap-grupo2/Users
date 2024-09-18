# from app.repositories.schemas import NewUser, User
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlalchemy.orm import Session

from . import models


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def insert_user(db: Session, new_user: models.User) -> models.User:
    # interests_list = [
    #     models.UserInterests(interest=schemas.Interests(interest))
    #     for interest in new_user.interests
    # ]
    db_user = models.User(
        id=uuid4(),
        email=new_user.email,
        user=new_user.user,
        name=new_user.name,
        location="",
        goals=[],
        interests=[],
        followers=[],
        twitsnaps=[]
        # location=new_user.location,
        # goals=[models.UsersGoals(goal=goal) for goal in new_user.goals],
        # interests=interests_list,
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
    
def get_user_by_email(db: Session, email: EmailStr) -> models.User: 
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def get_user_by_id(db: Session, user_id: UUID) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def empty_users(db: Session):
    db.query(models.User).delete()
    db.commit()


def set_location(db: Session, user_id: UUID, location: str): 
    updated_user = db.query(models.User).filter(models.User.id == user_id).update({'location': location})
    db.commit()
    return updated_user
    

def set_interests(db: Session, user_id: UUID, interests: list[models.UserInterests]): 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.interests.extend(interests)
        db.commit()
        db.refresh(user)
    return user

def set_goals(db: Session, user_id: UUID, goals: list[models.UsersGoals]): 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.goals.extend(goals)
        db.commit()
        db.refresh(user)
    return user

