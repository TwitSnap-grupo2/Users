from sqlalchemy import Column, ForeignKey, String, UUID, Table, Enum, text
from sqlalchemy.orm import relationship

from ..repositories.database import Base
from ..utils.schemas import Interests

# Association table for the many-to-many relationship
followers_table = Table(
    "followers",
    Base.metadata,
    Column(
        "follower_id",
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
    Column(
        "followed_id",
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String, unique=True, index=True)
    user = Column(String, unique=True)
    name = Column(String)
    location = Column(String)

    goals = relationship("UsersGoals", cascade="all, delete", back_populates="user")
    interests = relationship(
        "UserInterests", cascade="all, delete", back_populates="user"
    )
    # Users that this user is following

    followers = relationship(
        "User",
        secondary=followers_table,  # The association table
        primaryjoin=id == followers_table.c.followed_id,  # I'm being followed
        secondaryjoin=id == followers_table.c.follower_id,  # By someone else
        back_populates="followeds",  # The reverse relationship (who I follow)
        # single_parent=True,
        cascade="all, delete",
    )

    # Users that this user is following
    followeds = relationship(
        "User",
        secondary=followers_table,  # The same association table
        primaryjoin=id == followers_table.c.follower_id,  # I'm following someone
        secondaryjoin=id
        == followers_table.c.followed_id,  # They are being followed by me
        back_populates="followers",
        # backref="followers",  # The reverse relationship (who follows me)
        # single_parent=True,
        cascade="all, delete",
    )

    twitsnaps = relationship(
        "UserTwitsnaps", cascade="all, delete", back_populates="user"
    )


class UsersGoals(Base):
    __tablename__ = "users_goals"

    id_user = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )  # Foreign key to User table
    goal = Column(
        String, nullable=False, primary_key=True
    )  # The user's goal, part of the composite key

    user = relationship("User", back_populates="goals")


class UserInterests(Base):
    __tablename__ = "users_interests"

    id_user = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )  # Foreign key to User tablInterestse
    interest = Column(
        Enum(Interests),
        nullable=False,
        primary_key=True,
    )  # The user's interest, part of the composite key

    user = relationship("User", back_populates="interests")


class UserTwitsnaps(Base):
    __tablename__ = "users_twitsnaps"

    id_user = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    id_twitsnap = Column(UUID, primary_key=True)

    user = relationship("User", back_populates="twitsnaps")


class Admins(Base):
    __tablename__ = "admins"

    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True, index=True)


class UserDevices(Base):
    __tablename__ = "user_devices"

    id_user = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    device = Column(String)
