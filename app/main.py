from fastapi.responses import JSONResponse
from app.controllers import users
from fastapi import FastAPI, HTTPException
from app.repositories.schemas import SignUpSchema

app = FastAPI()


# import firebase_admin
# from firebase_admin import credentials, auth

# if not firebase_admin._apps:
#     cred = credentials.Certificate("serviceAccountKey.json")
#     firebase_admin.initialize_app(cred)

# firebase_config = {
#     "apiKey": "AIzaSyAS1_s8v-xZ8J6LBKRr09swSfLNY8Q_2Ag",
#     "authDomain": "twitsnapauth.firebaseapp.com",
#     "projectId": "twitsnapauth",
#     "storageBucket": "twitsnapauth.appspot.com",
#     "messagingSenderId": "722367291678",
#     "appId": "1:722367291678:web:1517b0758966229c0f690f",
#     "measurementId": "G-Z8T1KEJMW1",
#     "databaseURL": "",
# }

# firebase = pyrebase.initialize_app(firebase_config)

app.include_router(users.router)



