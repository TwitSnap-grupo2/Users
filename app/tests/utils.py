import os
from app.repositories import schemas, users, database
from app.services import users as users_service
from firebase_admin import auth

token = None

test_email=os.getenv("TEST_EMAIL")
test_password=os.getenv("TEST_PASSWORD")


def test_login():
    global token
    if not token:
        try: 
            users_service.signup(email=test_email, password=test_password)        
        except auth.EmailAlreadyExistsError:
            pass 
        finally:
            token = users_service.login(email=test_email, password=test_password)

def empty_database():
    db = next(database.get_db())
    users.empty_users(db=db)


def create_user(new_user: schemas.NewUser) -> schemas.User:
    db = next(database.get_db())
    return users_service.create_user(db=db, new_user=new_user)


def contains_values(expected_values, response_dict) -> bool:
    return all(item in response_dict.items() for item in expected_values.items())
