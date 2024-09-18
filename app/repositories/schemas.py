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


class DatabaseUser(BaseModel):
    email: EmailStr
    user: str
    name: str
    location: (
        str  
    ) = str()
    interests: list[Interest] = []
    goals: list[Goal] = []
    followers: list[Follower] = []
    twitsnaps: list[Twitsnap] = []


class NewUser(BaseModel):
    email: EmailStr
    user: str
    name: str



class User(NewUser):
    id: UUID
    location: (
        str  # TODO: change this for: CountryAlpha2 (Pydantic)
    ) 
    interests: list[Interests] 
    goals: list[str] 
    followers: list[UUID] 
    twitsnaps: list[UUID] 

    class Config:
        orm_mode = True


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
    user: str
    name: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoggedUser(User):
    token: str