from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories import users, models
from app.repositories.database import  engine
from pydantic_extra_types.country import CountryAlpha3
from app.utils import schemas
from pydantic import EmailStr
from app.utils.errors import ExistentUserError


models.Base.metadata.create_all(bind=engine)

def __database_model_to_schema(user: schemas.DatabaseUser) -> schemas.User:
    return schemas.User(
        id=user.id,
        email=user.email,
        user=user.user,
        name=user.name,
        location=user.location,
        goals=[g.goal for g in user.goals],
        interests=[schemas.Interests(interest.interest) for interest in user.interests],
        twitsnaps=[twitsnap.id_twitsnap for twitsnap in user.twitsnaps],
        followers=[follower.follower_id for follower in user.followers],
    )


# Use async because eventually it will be this way, so in order to make the refactor `cheaper` put it there for now
def fetch_users(db: Session) -> list[schemas.User]:
    db_users: list[schemas.DatabaseUser] = users.get_users(db)

    return [__database_model_to_schema(user) for user in db_users]


def fetch_user_by_id(db: Session, id: UUID) -> schemas.User | None:
    user: models.User = users.get_user_by_id(db=db, user_id=id)
    if user:
        return __database_model_to_schema(user)

def fetch_user_by_email(db: Session, email: EmailStr) -> schemas.User | None:
    user: models.User = users.get_user_by_email(db=db, email=email)
    if user:
        return __database_model_to_schema(user)


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



def set_location(db: Session, user_id: UUID, location: CountryAlpha3) -> schemas.User: 
    return __database_model_to_schema(users.set_location(db, user_id, str(location)))


def set_interests(db: Session, user_id: UUID, interests: list[schemas.Interests]) -> schemas.User: 
    interests_list = [
        models.UserInterests(interest=schemas.Interests(interest))
        for interest in interests
    ]
    return __database_model_to_schema(users.set_interests(db, user_id, interests_list))



def set_goals(db: Session, user_id: UUID, goals: list[str]) -> schemas.User: 
    goals_list = [
        models.UsersGoals(goal=goal)
        for goal in goals
    ]
    return __database_model_to_schema(users.set_goals(db, user_id, goals_list))

