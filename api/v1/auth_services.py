from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, EmailStr
import random
from datetime import datetime, timedelta
from database import get_db
from models.otp_model import OTP
from utils.email_utils import send_mail
from sqlalchemy.orm import Session
from sqlalchemy import and_

router = APIRouter()

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: int

@router.post("/request_otp", status_code=status.HTTP_200_OK)
async def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """
    Request OTP for email verification
    """
    try:
        # Check for recent OTP requests (rate limiting)
        recent_otp = db.query(OTP).filter(
            and_(
                OTP.email == request.email,
                OTP.created_at > datetime.utcnow() - timedelta(minutes=1)
            )
        ).first()
        
        if recent_otp:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Please wait before requesting another OTP"
            )
        
        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        
        # Send email
        result = send_mail(request.email, otp)
        
        if result["status"] == "error":
            print("EMAIL ERROR:", result["message"]) 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email"
            )
        
        # Delete any existing OTPs for this email
        db.query(OTP).filter(OTP.email == request.email).delete()
        
        # Create new OTP record
        new_otp = OTP(
            email=request.email,
            otp=otp,
            created_at=datetime.now(),
            expired_at=datetime.now() + timedelta(minutes=5),
            verified=False
        )
        
        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)
        
        return {
            "message": "OTP sent successfully",
            "email": request.email,
            "expires_in_minutes": 5
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.post("/verify_otp", status_code=status.HTTP_200_OK)
async def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP for email
    """
    try:
        # Find OTP record
        otp_record = db.query(OTP).filter(
            and_(
                OTP.email == request.email,
                OTP.otp == request.otp,
                OTP.verified == False
            )
        ).first()
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        # Check if OTP is expired
        if datetime.utcnow() > otp_record.expired_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )
        
        # Mark as verified
        otp_record.verified = True
        db.commit()
        
        return {
            "message": "OTP verified successfully",
            "email": request.email
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.delete("/cleanup_expired_otps", status_code=status.HTTP_200_OK)
async def cleanup_expired_otps(db: Session = Depends(get_db)):
    try:
        deleted_count = db.query(OTP).filter(
            OTP.expired_at < datetime.utcnow()
        ).delete()
        
        db.commit()
        
        return {
            "message": f"Cleaned up {deleted_count} expired OTP records"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )