from fastapi import APIRouter

from app.services.users import fetch_users

from app.repositories.models import User

# import app.repositories.models as db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> list[User]:
    return await fetch_users()


# @router.post("/")
# async def create_user():
