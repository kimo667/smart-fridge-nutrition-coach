from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import supabase

app = FastAPI(title="Smart Fridge & Nutrition Coach")


@app.get("/")
async def read_root():
    return {"message": "Smart Fridge & Nutrition Coach API is running"}


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
