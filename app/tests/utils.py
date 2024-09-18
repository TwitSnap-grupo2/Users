import os
from app.repositories import schemas, users, database
from app.services import users as users_service
from firebase_admin import auth

token = None

test_email=os.getenv("TEST_EMAIL")
test_password=os.getenv("TEST_PASSWORD")
test_user=os.getenv("TEST_USER")
test_name=os.getenv("TEST_NAME")


def test_login():
    global token
    if not token:
        try: 
            new_user = schemas.SignUpSchema(email=test_email, password=test_password, user=test_user, name=test_name) 
            users_service.signup(db=next(database.get_db()),  new_user=new_user)        
        except (auth.EmailAlreadyExistsError, users_service.ExistentUserError):
            pass 
        finally:
            token = users_service.login(db=next(database.get_db()), email=test_email, password=test_password).token

def empty_database():
    db = next(database.get_db())
    users.empty_users(db=db)


def create_user(new_user: schemas.NewUser) -> schemas.User:
    db = next(database.get_db())
    return users_service.create_user(db=db, new_user=new_user)


def contains_values(expected_values, response_dict) -> bool:
    return all(item in response_dict.items() for item in expected_values.items())
