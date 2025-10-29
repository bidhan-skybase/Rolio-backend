from datetime import datetime, timedelta, timezone

import jwt


SECRET_KEY="3660e2e232767cc198e4a775ce486335e31e77c8cba5913aae04c748e1d3425d"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 #7 DAYS


def create_access_token(data: dict| None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=1080)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt