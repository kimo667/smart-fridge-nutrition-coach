from fastapi import FastAPI

app = FastAPI(title="Smart Fridge & Nutrition Coach")


@app.get("/")
async def read_root():
    return {"message": "Smart Fridge & Nutrition Coach API is running"}
