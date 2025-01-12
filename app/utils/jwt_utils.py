from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException

# Change these in production and store in environment variables
SECRET_KEY = "7565488"
ALGORITHM = "HS256"

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    # No expiration time set, token will be valid indefinitely
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") 