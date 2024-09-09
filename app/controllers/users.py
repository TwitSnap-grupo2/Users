from fastapi import APIRouter, status
from app.services.users import fetch_users, create_user

from app.repositories.models import NewUser, User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> list[User]:
    return await fetch_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(new_user: NewUser) -> User:
    return await create_user(new_user)
