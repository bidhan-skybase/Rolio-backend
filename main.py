from fastapi import FastAPI
from database import Base, engine
from api.v1.users_services import router as users_router
from api.v1.auth_services import router as auth_router
from api.v1.jobs_services import router as job_router
from models import user_model, job_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rolio backend")

app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(job_router, prefix="/api/v1", tags=["jobs"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Rolio API"}