from datetime import datetime, timedelta
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database import Base


class OTP(Base):
    __tablename__="otps"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    otp=Column(Integer,index=True,nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    expired_at=Column(DateTime, default=datetime.now()+timedelta(minutes=5), nullable=False)
    verified=Column(Boolean,index=True)

