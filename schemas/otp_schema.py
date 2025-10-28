import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class OTPCreate(BaseModel):
    email:EmailStr
    otp:int
    created_at:datetime


class OTPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    email:str
    otp:int
    created_at:datetime
    expired_at:datetime
    verified:bool
    