from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.utils.errors import NotAllowed, UserNotFound
from ..repositories import models
from ..services import users as users_service
from sqlalchemy.orm import Session
from ..utils import schemas
from ..repositories.database import engine, get_db
from pydantic import EmailStr

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return users_service.fetch_users(db)


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
    user = users_service.fetch_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/email/{email}", response_model=schemas.User)
def get_user(email: EmailStr, db: Session = Depends(get_db)) -> schemas.User:
    user = users_service.fetch_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_account(user_data: schemas.SignUpSchema, db: Session = Depends(get_db)):
    try:
        user = users_service.signup(db=db, new_user=user_data)
        return user
    except users_service.ExistentUserError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post(
    "/location/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def set_location(
    user_id: UUID,
    location: schemas.Location = Body(example={"location": "ARG"}),
    db: Session = Depends(get_db),
):
    """
    - **location**: Location must be in  ISO 3166-1 alpha-3 format, e.g: ARG for Argentina.
    """
    try:
        return users_service.set_location(db, user_id, location.location)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "/interests/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def set_interests(
    user_id: UUID, interest_list: list[schemas.Interests], db: Session = Depends(get_db)
):
    try:
        return users_service.set_interests(db, user_id, interest_list)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "/goals/{user_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def set_goals(user_id: UUID, goals_list: list[str], db: Session = Depends(get_db)):
    try:
        return users_service.set_goals(db, user_id, goals_list)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/follow/{source_id}")
def follow(source_id: UUID, followed_id: UUID = Body(), db: Session = Depends(get_db)):
    if source_id == followed_id:
        raise HTTPException(status_code=403, detail="A user cannot follow himself")
    try:
        return users_service.follow(db=db, source_id=source_id, followed_id=followed_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except NotAllowed as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.delete("/follow/{source_id}")
def unfollow(
    source_id: UUID, followed_id: UUID = Body(), db: Session = Depends(get_db)
):
    if source_id == followed_id:
        raise HTTPException(status_code=403, detail="A user cannot unfollow himself")
    try:
        return users_service.unfollow(
            db=db, source_id=source_id, followed_id=followed_id
        )
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except NotAllowed as e:
        raise HTTPException(status_code=403, detail=e.message)
