from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import date, datetime

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

class ConditionBase(BaseModel):
    title: str
    description: str
    diagnosisDate: Optional[str] = Field(None, alias="diagnosis_date")
    medications: Optional[List[str]] = []

    @validator('diagnosisDate')
    def validate_diagnosis_date(cls, v):
        if not v:
            return None
        try:
            # Try to parse the date string
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format: {str(e)}")

    class Config:
        orm_mode = True
        populate_by_name = True
        allow_population_by_field_name = True

class ConditionCreate(ConditionBase):
    pass

class ConditionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    diagnosisDate: Optional[str] = Field(None, alias="diagnosis_date")
    medications: Optional[List[str]] = []

    @validator('diagnosisDate', pre=True)
    def format_date(cls, v):
        if isinstance(v, date):
            return v.isoformat()
        return v

    class Config:
        orm_mode = True
        populate_by_name = True
        allow_population_by_field_name = True 