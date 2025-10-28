from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr
import random
from datetime import datetime, timedelta
from utils.email_utils import send_mail

router = APIRouter()

otp_storage = {}

class EmailRequest(BaseModel):
    email: EmailStr

@router.post("/request_otp", status_code=status.HTTP_200_OK)
async def register_email(request: EmailRequest):
    try:
        otp = random.randint(100000, 999999)
        
        otp_storage[request.email] = {
            "otp": otp,
            "expires_at": datetime.now() + timedelta(minutes=5)
        }
        
        result = send_mail(request.email, otp)
        
        if result["status"] == "error":
            print("EMAIL ERROR:", result["message"]) 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP email"
            )
        
        return {
            "message": "OTP sent successfully",
            "email": request.email
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )