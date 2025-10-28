from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user_model import User  
from schemas.user_schema import UserCreate, UserDelete, UserResponse 

router = APIRouter()

@router.get("/users/", response_model=List[UserResponse],status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all() 
    return users 

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.delete("/users/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: UserDelete, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.id == user.id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()