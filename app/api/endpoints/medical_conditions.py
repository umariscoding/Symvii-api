from fastapi import APIRouter, HTTPException, Depends, Cookie
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.database.database import get_db
from app.models.models import MedicalCondition
from app.utils.jwt_utils import verify_jwt_token
from app.api.models.schemas import ConditionCreate, ConditionResponse
import uuid
import logging

router = APIRouter(prefix="/api/medical-conditions", tags=["Medical Conditions"])

@router.get("", response_model=List[ConditionResponse])
async def get_conditions(
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    conditions = db.query(MedicalCondition).filter(
        MedicalCondition.user_id == user_id
    ).all()
    
    return conditions
@router.post("", response_model=ConditionResponse)
async def create_condition(
    condition: ConditionCreate,
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    # Convert string date to date object if it exists
    diagnosis_date = None
    if condition.diagnosisDate:
        try:
            if isinstance(condition.diagnosisDate, date):
                diagnosis_date = condition.diagnosisDate
            else:
                # Parse the ISO format date string
                diagnosis_date = datetime.strptime(condition.diagnosisDate, '%Y-%m-%d').date()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    
    db_condition = MedicalCondition(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=condition.title,
        description=condition.description,
        diagnosis_date=diagnosis_date,
        medications=condition.medications or []
    )
    
    try:
        db.add(db_condition)
        db.commit()
        db.refresh(db_condition)
        return db_condition
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{condition_id}")
async def delete_condition(
    condition_id: str,
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    condition = db.query(MedicalCondition).filter(
        MedicalCondition.id == condition_id,
        MedicalCondition.user_id == user_id
    ).first()
    
    if not condition:
        raise HTTPException(status_code=404, detail="Condition not found")
    
    db.delete(condition)
    db.commit()
    return {"message": "Condition deleted successfully"} 