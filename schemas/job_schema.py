from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum

from models.job_model import JobStatus



class JobBase(BaseModel):
    title: str
    company: str
    logo: Optional[str] = None
    bg_color: Optional[str] = None
    salary: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: JobStatus = JobStatus.saved


class JobCreate(JobBase):
    pass


class JobBaseResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

