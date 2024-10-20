from fastapi import FastAPI
from app.routers import user_router
from app.routers import invoice_router

app = FastAPI()

app.include_router(user_router.router, prefix="/api", tags=["Users"])
app.include_router(invoice_router.router, prefix="/invoice", tags=["Invoice"])

@app.get("/")
async def root():
    return {"message": "Raghul OKR project!"}
