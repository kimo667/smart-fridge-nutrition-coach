from fastapi import FastAPI
from pydantic import BaseModel

from app.core.security import supabase

app = FastAPI(title="Smart Fridge & Nutrition Coach")


class UserAuth(BaseModel):
    email: str
    password: str


@app.get("/")
async def read_root():
    return {"message": "Smart Fridge & Nutrition Coach API is running"}


@app.post("/register")
async def register(user: UserAuth):
    response = supabase.auth.sign_up({"email": user.email, "password": user.password})
    return response


@app.post("/login")
async def login(user: UserAuth):
    response = supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})
    return response
