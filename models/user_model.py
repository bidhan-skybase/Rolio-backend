from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from database import Base

class User(Base):  
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)