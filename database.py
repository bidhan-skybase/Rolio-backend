from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

db_url = "postgresql://postgres:1234@localhost:5432/rolio"

engine = create_engine(
    db_url,
    pool_pre_ping=True,  
    echo=False 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()