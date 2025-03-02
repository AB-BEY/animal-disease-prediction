from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Diagnosis
from schemas import HistoryResponse

router = APIRouter()

@router.get("/reports/{user_id}", response_model=HistoryResponse)
async def history_report(user_id: int,db: Session = Depends(get_db)):
    history_table = db.exec(select(Diagnosis).where(Diagnosis.id==user_id)).all()
    return history_table

@router.delete("/reports/delete")
async def delete_diagnosis(diagnosis_ids: list[int], db: Session = Depends(get_db)):
    diagnosis = db.exec(select(Diagnosis).where(Diagnosis.id.in_(diagnosis_ids))).all()

    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis report not found")

    db.delete(diagnosis)
    db.commit()
    remaining_diagnoses = db.exec(select(Diagnosis)).all()
    return remaining_diagnoses
