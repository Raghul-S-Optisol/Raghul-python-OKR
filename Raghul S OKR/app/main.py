from fastapi import FastAPI
from app.routers import user_router

app = FastAPI()

app.include_router(user_router.router, prefix="/api", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Raghul OKR project!"}
