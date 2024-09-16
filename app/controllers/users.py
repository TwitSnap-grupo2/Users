from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories import models
from app.services.users import fetch_users, create_user
from sqlalchemy.orm import Session
from app.repositories import schemas
from app.repositories.database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return fetch_users(db)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def post_user(new_user: schemas.NewUser, db: Session = Depends(get_db)):
    return create_user(db, new_user)


# @router.get("/{user_id}")
# async def get_user(user_id: UUID) -> User:
#     user = await fetch_user(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
