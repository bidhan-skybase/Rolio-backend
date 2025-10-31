from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as PgEnum
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from enum import Enum
from database import Base


class JobStatus(str, Enum):
    saved="saved"
    applied='applied'
    interview='interview'
    rejected='rejected'
    offered='offered'


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    bg_color = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(PG_ARRAY(String), nullable=True)
    status = Column(PgEnum(JobStatus, name="job_status_enum"), nullable=False, default=JobStatus.saved)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="jobs")
