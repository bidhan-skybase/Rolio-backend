import datetime
from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime