from pydantic import BaseModel
from enum import Enum
from uuid import UUID


class Interests(str, Enum):
    sports = "sports"
    games = "games"
    science = "science"
    politics = "politics"
    engineering = "engineering"


# TODO: complete this
# user refers to the login name, where name refers to the displayed name inside the app
class User(BaseModel):
    id: str
    user: str
    name: str
    location: (
        str  # TODO: check if there exists a model that provides fixed geolocations
    )
    interests: list[Interests]
    # goals: list[str]
    # blocked: bool
    # followed_accounts: list[UUID]
    # followed_by: list[UUID]
    # followed_hashtags: list[str] # TODO: verify if the hashtag is identified by its name (will surely be)
    # twit_snaps: list[]
    # snap_shares: list[]
    # favorites: list[]
