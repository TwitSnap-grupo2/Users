# from app.repositories.schemas import NewUser, User
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.orm import Session

from app.utils import schemas
from app.utils.errors import NotAllowed, UserNotFound

from . import models

# import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def search_users(db: Session, query: str, limit: int) -> list[models.User]:
    return (
        db.query(models.User)
        .filter(func.similarity(models.User.user, query) > 0.1)
        .order_by(func.similarity(models.User.user, query).desc())
        .limit(limit)
        .all()
    )


def insert_user(db: Session, new_user: models.User) -> models.User:
    db_user = models.User(
        id=uuid4(),
        email=new_user.email,
        user=new_user.user,
        name=new_user.name,
        location=new_user.location,
        goals=[],
        interests=[],
        followers=[],
        followeds=[],
        twitsnaps=[],
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def insert_admin(db: Session, new_admin: models.Admins) -> models.Admins:
    db_admin = models.Admins(
        id=uuid4(),
        email=new_admin.email,
    )

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_user_by_email_or_name(db: Session, email: EmailStr, user: str) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.email == email or models.User.user == user)
        .first()
    )


def get_admin_by_email(db: Session, email: EmailStr) -> models.Admins:
    return db.query(models.Admins).filter(models.Admins.email == email).first()


def get_user_by_email(db: Session, email: EmailStr) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def get_admin_by_id(db: Session, admin_id: UUID) -> models.Admins:
    admin = db.query(models.Admins).filter(models.Admins.id == admin_id).first()
    return admin


def search_followeds(
    db: Session, user_id: UUID, query: str, limit: int
) -> list[models.User]:
    user: models.User = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")
    followeds = [followed.id for followed in user.followeds]
    return (
        db.query(models.User)
        .filter(models.User.id.in_(followeds))
        .filter(func.similarity(models.User.user, query) > 0.1)
        .order_by(func.similarity(models.User.user, query).desc())
        .limit(limit)
        .all()
    )


def empty_users(db: Session):
    db.query(models.User).delete()
    db.query(models.Admins).delete()
    db.commit()


def set_location(db: Session, user_id: UUID, location: str) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound()

    user.location = location
    db.commit()
    db.refresh(user)
    return user


def set_interests(
    db: Session, user_id: UUID, interests: list[models.UserInterests]
) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound()

    user.interests.extend(interests)
    db.commit()
    db.refresh(user)
    return user


def set_goals(db: Session, user_id: UUID, goals: list[models.UsersGoals]):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFound()

    user.goals.extend(goals)
    db.commit()
    db.refresh(user)

    return user


def __user_is_following(follower_user: models.User, followed_user: models.User) -> bool:
    return True if followed_user in frozenset(follower_user.followeds) else False


def add_follower(db: Session, source_id: UUID, followed_id: str) -> models.User:
    source_user = get_user_by_id(db=db, user_id=source_id)

    if not source_user:
        raise UserNotFound("Follower user not found")

    followed_user = get_user_by_id(db=db, user_id=followed_id)

    if not followed_user:
        raise UserNotFound("Followed user not found")

    if __user_is_following(follower_user=source_user, followed_user=followed_user):
        raise NotAllowed(message=f"The user is already following {followed_user.name}")

    followed_user.followers.append(source_user)

    db.commit()
    db.refresh(followed_user)
    db.refresh(source_user)

    return source_user


def remove_follow(db: Session, source_id: UUID, followed_id: str) -> models.User:
    source_user = get_user_by_id(db=db, user_id=source_id)

    if not source_user:
        raise UserNotFound("Follower user not found")

    followed_user = get_user_by_id(db=db, user_id=followed_id)

    if not followed_user:
        raise UserNotFound("Followed user not found")

    if not __user_is_following(follower_user=source_user, followed_user=followed_user):
        raise NotAllowed(
            message=f"Cannot unfollow an unfollowed user: {followed_user.name}"
        )

    if followed_user in source_user.followeds:
        source_user.followeds.remove(followed_user)

    db.commit()
    db.refresh(followed_user)
    db.refresh(source_user)

    return source_user


def get_followers(db: Session, user_id: UUID) -> models.User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")
    return user.followers


def get_followeds(db: Session, user_id: UUID) -> models.User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")
    return user.followeds


def update_name(db: Session, user_id: UUID, name: str) -> models.User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")
    user.name = name
    db.commit()
    db.refresh(user)
    return user


def get_recommendations(db: Session, user_id: UUID) -> list[models.User]:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")

    statement = text(
        """
            WITH direct_followed AS (
                SELECT followed_id
                FROM followers
                WHERE follower_id =:user_id
            )
            SELECT users.id, users.name, users.user
            FROM direct_followed df
            JOIN followers uf ON df.followed_id = uf.follower_id
            JOIN users ON (uf.followed_id=users.id) 
            WHERE uf.followed_id NOT IN (
                SELECT followed_id
                FROM followers
                WHERE follower_id =:user_id
            )
            UNION
            SELECT u1.id, u1.name, u1.user FROM users u1
            JOIN users_interests ui ON (u1.id = ui.id_user)
            WHERE ui.interest IN (
            SELECT ui.interest FROM users u
            JOIN users_interests ui ON (u.id = ui.id_user)
            WHERE u.id =:user_id
            ) 
            AND u1.id !=:user_id
            UNION
            SELECT u1.id, u1.name, u1.user FROM users u1
            WHERE u1.location =:user_location
            AND u1.id !=:user_id
                     """
    )
    result = db.execute(statement, {"user_id": user.id, "user_location": user.location})

    recommendations = [dict(row) for row in result.mappings()]

    return recommendations


def modify_block_status(db: Session, user_id: UUID, block_status: bool):
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound("No user was found for the given id")

    user.is_blocked = block_status
    db.commit()
    db.refresh(user)
    return user


# For testing purposes
def _insert_user(db: Session, new_user: schemas.UserWithoutId) -> models.User:
    db_user = models.User(
        id=uuid4(),
        email=new_user.email,
        user=new_user.user,
        name=new_user.name,
        location=new_user.location,
        goals=new_user.goals,
        interests=[
            models.UserInterests(interest=schemas.Interests(interest))
            for interest in new_user.interests
        ],
        followers=new_user.followers,
        followeds=new_user.followeds,
        twitsnaps=new_user.twitsnaps,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
