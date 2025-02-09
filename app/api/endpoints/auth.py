from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import User
from app.utils.jwt_utils import create_jwt_token, verify_jwt_token
from app.api.models.schemas import UserLogin, UserSignup, UserUpdate
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user_response = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "country": user.country
    }
    
    token = create_jwt_token({"user_id": user.id})
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=31536000
    )
    
    return {"user": user_response}

@router.post("/signup")
async def signup(user_data: UserSignup, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        phone=user_data.phone,
        country=user_data.country
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_response = {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "phone": new_user.phone,
        "country": new_user.country
    }
    
    token = create_jwt_token({"user_id": new_user.id})
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=31536000
    )
    
    return {"user": user_response}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="session",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Successfully logged out"}

@router.put("/update-profile")
async def update_profile(
    user_data: UserUpdate,
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    user.name = user_data.name
    user.phone = user_data.phone
    user.country = user_data.country
    
    db.commit()
    
    user_response = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "country": user.country
    }
    
    return {"user": user_response}

@router.get("/session")
async def check_session(
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = verify_jwt_token(session)
        user_id = payload.get("user_id")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        user_response = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "country": user.country
        }
        
        return {"user": user_response}
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid session") 