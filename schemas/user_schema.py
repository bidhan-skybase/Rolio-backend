from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class User(Base):
    __tablename__='User'
    id=Column(primary_key=True,index=True,autoincrement=True)
