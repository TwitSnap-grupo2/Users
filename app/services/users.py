from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories import users, models
from app.repositories.database import engine
from pydantic_extra_types.country import CountryAlpha3
from app.utils import schemas
from pydantic import EmailStr
from app.utils.errors import BlockedUser, ExistentUserError


models.Base.metadata.create_all(bind=engine)


def __database_model_to_schema(user: schemas.DatabaseUser) -> schemas.User:
    return schemas.User(
        id=user.id,
        email=user.email,
        user=user.user,
        name=user.name,
        is_blocked=user.is_blocked,
        location=user.location,
        goals=[g.goal for g in user.goals],
        interests=[schemas.Interests(interest.interest) for interest in user.interests],
        twitsnaps=[twitsnap.id_twitsnap for twitsnap in user.twitsnaps],
        followers=[follower.id for follower in user.followers],
        followeds=[followed.id for followed in user.followeds],
    )


def __database_model_to_admin_schema(user: models.Admins) -> schemas.Admin:
    return schemas.Admin(
        id=user.id,
        email=user.email,
    )


def fetch_users(db: Session) -> list[schemas.User]:
    db_users: list[schemas.DatabaseUser] = users.get_users(db)

    return [__database_model_to_schema(user) for user in db_users]


def fetch_user_by_id(db: Session, id: UUID) -> schemas.User | None:
    user: models.User = users.get_user_by_id(db=db, user_id=id)
    print("user: {user}")

    if user:
        if user.is_blocked:
            raise BlockedUser
        return __database_model_to_schema(user)


def fetch_user_by_email(db: Session, email: EmailStr) -> schemas.User | None:
    user: models.User = users.get_user_by_email(db=db, email=email)
    if user:
        if user.is_blocked:
            raise BlockedUser
        return __database_model_to_schema(user)


def search_users(db: Session, user: str, limit: int) -> list[schemas.User]:
    db_users: list[schemas.DatabaseUser] = users.search_users(db, user, limit)
    return [__database_model_to_schema(user) for user in db_users]


def search_followeds(
    db: Session, user_id: UUID, user: str, limit: int
) -> list[schemas.User]:
    db_users: list[schemas.DatabaseUser] = users.search_followeds(
        db, user_id, user, limit
    )
    return [__database_model_to_schema(user) for user in db_users]


def signup(db: Session, new_user: schemas.SignUpSchema) -> schemas.User:
    user = users.get_user_by_email_or_name(
        db=db, email=new_user.email, user=new_user.user
    )

    if not user:
        # _res = firebase_admin.auth.create_user(email=str(new_user.email), password=new_user.password)
        db_user = users.insert_user(db=db, new_user=new_user)
        return __database_model_to_schema(db_user)

    # If here, then the user exists, so check for email or user repetition
    if user.email == new_user.email:
        raise ExistentUserError("Mail is already registered")
    if user.user == new_user.user:
        raise ExistentUserError("Username is already registered")


def signup_admin(db: Session, new_admin: schemas.SignUpAdminSchema) -> schemas.Admin:
    admin = users.get_admin_by_email(db=db, email=new_admin.email)

    if not admin:
        db_admin = users.insert_admin(db=db, new_admin=new_admin)
        return __database_model_to_admin_schema(db_admin)

    if admin.email == new_admin.email:
        raise ExistentUserError("Mail is already registered")


def fetch_admin_by_id(db: Session, id: UUID) -> schemas.Admin | None:
    admin: models.Admins = users.get_admin_by_id(db=db, admin_id=id)
    if admin:
        return __database_model_to_admin_schema(admin)


def set_location(db: Session, user_id: UUID, location: CountryAlpha3) -> schemas.User:
    return __database_model_to_schema(users.set_location(db, user_id, str(location)))


def set_interests(
    db: Session, user_id: UUID, interests: list[schemas.Interests]
) -> schemas.User:
    interests_list = [
        models.UserInterests(interest=schemas.Interests(interest))
        for interest in interests
    ]
    return __database_model_to_schema(users.set_interests(db, user_id, interests_list))


def set_goals(db: Session, user_id: UUID, goals: list[str]) -> schemas.User:
    goals_list = [models.UsersGoals(goal=goal) for goal in goals]
    return __database_model_to_schema(users.set_goals(db, user_id, goals_list))


def follow(db: Session, source_id: UUID, followed_id: str) -> schemas.User:
    return __database_model_to_schema(
        users.add_follower(db=db, source_id=source_id, followed_id=followed_id)
    )


def unfollow(db: Session, source_id: UUID, followed_id: str) -> schemas.User:
    return __database_model_to_schema(
        users.remove_follow(db=db, source_id=source_id, followed_id=followed_id)
    )


def get_followers(db: Session, user_id: UUID) -> list[schemas.User]:
    return [
        __database_model_to_schema(user) for user in users.get_followers(db, user_id)
    ]


def get_followeds(db: Session, user_id: UUID) -> list[schemas.User]:
    return [
        __database_model_to_schema(user) for user in users.get_followeds(db, user_id)
    ]


def update_name(db: Session, user_id: UUID, name: str) -> schemas.User:
    return __database_model_to_schema(users.update_name(db, user_id, name))


def get_recommendations(db: Session, user_id: UUID) -> schemas.User:
    return [
        schemas.RecommendationUser(id=user["id"], user=user["user"], name=user["name"])
        for user in users.get_recommendations(db, user_id)
    ]


def block_user(db: Session, user_id: UUID) -> schemas.User:
    return __database_model_to_schema(
        users.modify_block_status(db, user_id, block_status=True)
    )


def unblock_user(db: Session, user_id: UUID) -> schemas.User:
    return __database_model_to_schema(
        users.modify_block_status(db, user_id, block_status=False)
    )
