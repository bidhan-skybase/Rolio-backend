from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from database import get_db
from models import user_model
from schemas.token_schema import TokenResponse


# Constants
SECRET_KEY = "3660e2e232767cc198e4a775ce486335e31e77c8cba5913aae04c748e1d3425d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

# Security scheme (for Swagger UI)
oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=True)

# -------------------------------
# CREATE ACCESS TOKEN
# -------------------------------
def create_access_token(data: dict | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(
        token=encoded_jwt,
        token_type="Bearer",
        token_expiry=expire
    )


# -------------------------------
# VERIFY TOKEN
# -------------------------------

def verify_access_token(token: str):
    try:
        # Remove "Bearer " prefix if provided
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user_id: str = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

