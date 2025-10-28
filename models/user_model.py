import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    email: str
    created_at: datetime