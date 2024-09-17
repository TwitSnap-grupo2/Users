from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from app.repositories import models
from app.services import users as users_service
from sqlalchemy.orm import Session
from app.repositories import schemas
from app.repositories.database import engine, get_db
from firebase_admin import auth
import firebase_admin
from app.utils.firebase import firebase
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token




models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])

# use of a simple bearer scheme as auth is handled by firebase and not fastapi
# we set auto_error to False because fastapi incorrectly returns a 403 intead 
# of a 401
# see: https://github.com/tiangolo/fastapi/pull/2120
bearer_scheme = HTTPBearer(auto_error=False)

def get_firebase_user_from_token(
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> dict | None:
    """Uses bearer token to identify firebase user id
    Args:
        token : the bearer token. Can be None as we set auto_error to False
    Returns:
        dict: the firebase user on success
    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """
    try:
        if not token:
            # raise and catch to return 401, only needed because fastapi returns 403
            # by default instead of 401 so we set auto_error to False
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user
    # lots of possible exceptions, see firebase_admin.auth,
    # but most of the time it is a credentials issue
    except Exception:
        # we also set the header
        # see https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        
        
@router.get("/", response_model=list[schemas.User])
def get_users(_user: Annotated[dict, Depends(get_firebase_user_from_token)], db: Session = Depends(get_db)):
    return users_service.fetch_users(db)


# TODO: no se puede acceder a este endpoint si no esta loggeado
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def post_user(_user: Annotated[dict, Depends(get_firebase_user_from_token)], new_user: schemas.NewUser, db: Session = Depends(get_db)):
    try:
        user = users_service.create_user(db, new_user)
        return user
    except users_service.ExistentUserError as e:
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail=e.message,
        )


@router.get("/{user_id}", response_model=schemas.User)
def get_user(_user: Annotated[dict, Depends(get_firebase_user_from_token)], user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
    user = users_service.fetch_user_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/signup")
def create_account(user_data: schemas.SignUpSchema):
    try:
        email = str(user_data.email)
        password = user_data.password
        # user = firebase_admin.auth.create_user(email=email, password=password)

        user = users_service.signup(email, password)

        return JSONResponse(
            content={
                "message": f"User account created successfuly for user: {user.uid}"
            },
            status_code=201,
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400, detail=f"Account already created for: {email}"
        )

@router.post("/login")
async def create_access_token(user_data:schemas.LoginSchema):
    email = str(user_data.email)
    password = user_data.password
    try:
        token = users_service.login(email=email, password=password)
        
        return JSONResponse(
            content={
                "token":token
            },status_code=200
        )

    except:
        raise HTTPException(
            status_code=400,detail="Invalid Credentials"
        )
