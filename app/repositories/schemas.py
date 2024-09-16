from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID


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

    class Config:
        orm_mode = True


class Goal(BaseModel):
    goal: str

    class Config:
        orm_mode = True


class Interest(BaseModel):
    interest: Interests

    class Config:
        orm_mode = True


class Follower(BaseModel):
    follower_id: UUID

    class Config:
        orm_mode = True


class Twitsnap(BaseModel):
    id_twitsnap: UUID

    class Config:
        orm_mode = True


class NewUser(BaseModel):
    email: EmailStr
    user: str
    name: str
    location: (
        str  # TODO: check if there exists a model that provides fixed geolocations
    )
    interests: list[Interest] = []
    goals: list[Goal] = []
    followers: list[Follower] = []
    twitsnaps: list[UUID] = []


class User(NewUser):
    id: UUID

    class Config:
        orm_mode = True
