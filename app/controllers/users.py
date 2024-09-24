from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from ..repositories import models
from ..services import users as users_service
from sqlalchemy.orm import Session
from ..utils import schemas
from ..repositories.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])

        
@router.get("/", response_model=list[schemas.User])
# def get_users(_user: Annotated[dict, Depends(get_firebase_user_from_token)], db: Session = Depends(get_db)):
def get_users(db: Session = Depends(get_db)):
    return users_service.fetch_users(db)




@router.get("/{user_id}", response_model=schemas.User)
# def get_user(_user: Annotated[dict, Depends(get_firebase_user_from_token)], user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
    user = users_service.fetch_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_account(user_data: schemas.SignUpSchema, db: Session = Depends(get_db)):
    try:
        user = users_service.signup(db=db, new_user=user_data)
        return user
    except users_service.ExistentUserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message 
        )


# def set_location(_user: Annotated[dict, Depends(get_firebase_user_from_token)], user_id: UUID, location: CountryAlpha3, db: Session = Depends(get_db)): 
@router.post("/location/{user_id}", status_code=status.HTTP_201_CREATED)
def set_location(user_id: UUID, location: schemas.Location = Body(example={"location": "ARG"}), db: Session = Depends(get_db)): 
    """ 
    - **location**: Location must be in  ISO 3166-1 alpha-3 format, e.g: ARG for Argentina.
    """

    return users_service.set_location(db, user_id, location.location) 



@router.post("/interests/{user_id}", status_code=status.HTTP_201_CREATED)
def set_interests(user_id: UUID, interest_list: list[schemas.Interests], db: Session = Depends(get_db)): 
    return users_service.set_interests(db, user_id, interest_list)



@router.post("/goals/{user_id}", status_code=status.HTTP_201_CREATED)
def set_goals(user_id: UUID, goals_list:list[str], db: Session = Depends(get_db)): 
    return users_service.set_goals(db, user_id, goals_list)
