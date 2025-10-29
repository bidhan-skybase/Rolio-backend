from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class TokenResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    token:str
    token_type:str
    token_expiry:datetime
