from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories import models
from app.services import users as users_service

# from app.services.users import ExistentUserError, fetch_users, create_user
from sqlalchemy.orm import Session
from app.repositories import schemas
from app.repositories.database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):

    return users_service.fetch_users(db)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def post_user(new_user: schemas.NewUser, db: Session = Depends(get_db)):
    try:
        user = users_service.create_user(db, new_user)
        return user
    except users_service.ExistentUserError as e:
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail=e.message,
        )


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
    user = users_service.fetch_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
