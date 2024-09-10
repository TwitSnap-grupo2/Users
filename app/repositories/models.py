from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID


class Interests(str, Enum):
    sports = "sports"
    games = "games"
    science = "science"
    politics = "politics"
    engineering = "engineering"


class NewUser(BaseModel):
    email: EmailStr  # Must be unique
    user: str  # Must be unique
    name: str  # Must be unique
    location: (
        str  # TODO: check if there exists a model that provides fixed geolocations
    )
    interests: list[Interests]
    goals: list[str]
    blocked: bool = False
    followed_accounts: list[UUID] = []
    followed_by: list[UUID] = []
    followed_hashtags: list[str] = (
        []
    )  # TODO: verify if the hashtag is identified by its name (will surely be)
    twit_snaps: list[str] = []
    snap_shares: list[str] = []
    favorites: list[str] = []


class User(NewUser):
    id: UUID
