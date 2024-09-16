from sqlalchemy import Column, ForeignKey, String, UUID, Table, Enum, text
from sqlalchemy.orm import relationship

from app.repositories.database import Base
from app.repositories.schemas import Interests

# Association table for the many-to-many relationship
followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", UUID, ForeignKey("users.id"), primary_key=True),
)


# user1.followed.append(user2)  # user1 follows user2
# session.commit()
# --------------------------------
# followers_of_user1 = user1.followers  # Get all users following user1


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String, unique=True, index=True)
    user = Column(String, unique=True)
    name = Column(String)
    location = Column(String)

    goals = relationship("UsersGoals", back_populates="user")
    interests = relationship("UserInterests", back_populates="user")
    # Users that this user is following
    followers = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        # backref="followers",
        back_populates="followers",
    )

    twitsnaps = relationship("UserTwitsnaps", back_populates="user")


class UsersGoals(Base):
    __tablename__ = "users_goals"

    id_user = Column(
        UUID, ForeignKey("users.id"), primary_key=True
    )  # Foreign key to User table
    goal = Column(
        String, nullable=False, primary_key=True
    )  # The user's goal, part of the composite key

    user = relationship("User", back_populates="goals")


class UserInterests(Base):
    __tablename__ = "users_interests"

    id_user = Column(
        UUID, ForeignKey("users.id"), primary_key=True
    )  # Foreign key to User tablInterestse
    interest = Column(
        Enum(Interests),
        nullable=False,
        primary_key=True,
    )  # The user's interest, part of the composite key

    user = relationship("User", back_populates="interests")


class UserTwitsnaps(Base):
    __tablename__ = "users_twitsnaps"

    id_user = Column(UUID, ForeignKey("users.id"), primary_key=True)
    id_twitsnap = Column(UUID, primary_key=True)

    user = relationship("User", back_populates="twitsnaps")
