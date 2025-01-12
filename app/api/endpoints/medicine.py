from fastapi import APIRouter, HTTPException, Depends, Cookie
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import MedicineGraph
from app.utils.jwt_utils import verify_jwt_token

router = APIRouter(prefix="/api/medicine-graphs", tags=["Medicine"])

@router.post("")
async def save_medicine_graphs(
    graphs: List[dict],
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    db.query(MedicineGraph).filter(MedicineGraph.user_id == user_id).delete(synchronize_session=False)
    
    for graph in graphs:
        data = sorted(graph.get("data", []), key=lambda x: x.get("date", ""))
        
        new_graph = MedicineGraph(
            id=graph.get("id"),
            name=graph.get("name"),
            data=data,
            user_id=user_id
        )
        db.add(new_graph)
    
    db.commit()
    return {"message": "Graphs saved successfully"}

@router.get("")
async def get_graphs(
    session: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_jwt_token(session)
    user_id = payload.get("user_id")
    
    graphs = db.query(MedicineGraph).filter(MedicineGraph.user_id == user_id).all()
    
    return [
        {
            "id": graph.id,
            "name": graph.name,
            "data": sorted(graph.data, key=lambda x: x.get("date", "")),
            "user_id": graph.user_id
        }
        for graph in graphs
    ] 