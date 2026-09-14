from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import supabase, SECRET_KEY, ALGORITHM
from app.core.metabolism import UserProfile, calculer_profil_complet

app = FastAPI(title="Smart Fridge & Nutrition Coach")


@app.get("/")
async def read_root():
    return {"message": "Smart Fridge & Nutrition Coach API is running"}


@app.post("/profil")
async def calculer_profil(profil: UserProfile):
    return calculer_profil_complet(profil)


@app.post("/signup")
def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = supabase.table("users").select("*").eq("username", form_data.username).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user_data = {
        "username": form_data.username,
        "password": form_data.password,
    }
    new_user = supabase.table("users").insert(new_user_data).execute()
    return {"message": "User registered successfully"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    response = supabase.table("users").select("*").eq("username", form_data.username).execute()
    users_list = response.data

    if not users_list or users_list[0]["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect ids in the database")

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": form_data.username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
