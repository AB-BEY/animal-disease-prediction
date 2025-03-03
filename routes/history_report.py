from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Diagnosis, Animal
from schemas import HistoryResponse

router = APIRouter()

@router.get("/reports/{user_id}", response_model=list[HistoryResponse])
async def history_report(user_id: int,db: Session = Depends(get_db)):
    statement = (
        select(Diagnosis)
        .join(Animal)
        .where(Animal.user_id == user_id)
    )
    history_table = db.exec(statement).all()
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
