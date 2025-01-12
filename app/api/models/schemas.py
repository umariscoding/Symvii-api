from pydantic import BaseModel
from typing import Optional

class DosageData(BaseModel):
    day: str
    dosage: float
    symptom: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    phone: str
    country: str

class UserUpdate(BaseModel):
    name: str
    phone: str
    country: str 