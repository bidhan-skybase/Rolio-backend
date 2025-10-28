from fastapi import FastAPI
from database import Base, engine
from api.v1.users_services import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rolio backend")

app.include_router(users_router, prefix="/api/v1", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Rolio API"}