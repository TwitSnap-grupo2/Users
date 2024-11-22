from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID
from pydantic_extra_types.country import CountryAlpha3


class Interests(str, Enum):
    sports = "sports"
    games = "games"
    science = "science"
    politics = "politics"
    engineering = "engineering"


class UserSummary(BaseModel):
    id: UUID
    user: str  # User's username
    name: str  # User's full name

    class ConfigDict:
        from_attributes = True


class DatabaseGoal(BaseModel):
    goal: str

    class ConfigDict:
        from_attributes = True


class DatabaseInterest(BaseModel):
    interest: Interests

    class ConfigDict:
        from_attributes = True


class DatabaseFollower(BaseModel):
    follower_id: UUID

    class ConfigDict:
        from_attributes = True


class DatabaseTwitsnap(BaseModel):
    id_twitsnap: UUID

    class ConfigDict:
        from_attributes = True


class NewUser(BaseModel):
    email: EmailStr
    user: str
    name: str
    location: str


class User(NewUser):
    id: UUID
    location: str
    interests: list[Interests]
    goals: list[str]
    followers: list[UUID]
    followeds: list[UUID]
    twitsnaps: list[UUID]
    is_blocked: bool


class DatabaseUser(BaseModel):
    id: UUID
    email: EmailStr
    user: str
    name: str
    location: str = str()
    interests: list[DatabaseInterest] = []
    goals: list[DatabaseGoal] = []
    followers: list[User] = []
    followeds: list[User] = []
    twitsnaps: list[DatabaseTwitsnap] = []
    is_blocked: bool


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
    user: str
    name: str
    location: str


class SignUpAdminSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoggedUser(User):
    token: str


class Location(BaseModel):
    location: CountryAlpha3


class Admin(BaseModel):
    id: UUID
    email: EmailStr


class RecommendationUser(BaseModel):
    id: UUID
    user: str
    name: str


class UserWithoutId(NewUser):
    location: str
    interests: list[Interests]
    goals: list[str]
    followers: list[UUID]
    followeds: list[UUID]
    twitsnaps: list[UUID]
