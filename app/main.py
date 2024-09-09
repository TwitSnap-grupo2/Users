from fastapi import FastAPI
from app.controllers import users


app = FastAPI()

app.include_router(users.router)
