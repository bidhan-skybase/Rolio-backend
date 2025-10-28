import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(primary_key=True,index=True,autoincrement=True)
    email=Column(String,unique=True,index=True,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
