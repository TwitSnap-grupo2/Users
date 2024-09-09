from fastapi import APIRouter

from app.services.users import fetch_users, create_user

from app.repositories.models import NewUser, User

# import app.repositories.models as db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> list[User]:
    return await fetch_users()


@router.post("/")
async def post_user(new_user: NewUser) -> User:
    return await create_user(new_user)
