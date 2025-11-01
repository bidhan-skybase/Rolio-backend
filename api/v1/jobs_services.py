from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from database import get_db
from models.job_model import Job
from schemas.job_schema import JobBaseResponse, JobCreate
from utils.token_utils import get_current_user

router = APIRouter(
)


# -------------------------------
# Create Job
# -------------------------------
@router.post("/create", response_model=JobBaseResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_job = Job(**job.model_dump())
    new_job.user_id = user.id

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


# -------------------------------
# List Jobs (User Specific)
# -------------------------------
@router.get("/list", response_model=List[JobBaseResponse], status_code=status.HTTP_200_OK)
def list_jobs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    jobs = (
        db.query(Job)
        .filter(Job.user_id == user.id)
        .order_by(Job.created_at.desc())
        .all()
    )
    return jobs


# -------------------------------
# Update Job Status
# -------------------------------



@router.patch("/{job_id}/status", response_model=JobBaseResponse)
def update_job_status(
    job_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if status_value not in ["applied", "interview", "offered",'saved','rejected']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value")

    job.status = status_value
    db.commit()
    db.refresh(job)
    return job


# -------------------------------
# Delete Job
# -------------------------------
@router.delete("/delete/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()
    return None

@router.get("/stats", status_code=status.HTTP_200_OK, response_model=dict)
def get_dashboard_stats(
    jobs=Depends(list_jobs)  
):
    saved = applied = offered = 0
    for job in jobs:
        if job.status == 'saved':
            saved += 1
        elif job.status == 'applied':
            applied += 1
        elif job.status == 'offered':
            offered += 1
    return {
        "saved": saved,
        "applied": applied,
        "offered": offered
    }
