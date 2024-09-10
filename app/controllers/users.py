from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.services.users import fetch_users, create_user, fetch_user

from app.repositories.models import NewUser, User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> list[User]:
    return await fetch_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(new_user: NewUser) -> User:
    return await create_user(new_user)


@router.get("/{user_id}")
async def get_user(user_id: UUID) -> User:
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
