from fastapi import FastAPI
from database import Base, engine
from api.v1.users_services import router as users_router
from api.v1.auth_services import router as auth_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rolio backend")

app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Rolio API"}