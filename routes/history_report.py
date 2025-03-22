from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Diagnosis, Animal, User
from schemas import HistoryResponse, DiagnosisDeleteRequest

router = APIRouter()

@router.get("/reports/{id}", response_model=list[HistoryResponse])
async def history_report(id: int,db: Session = Depends(get_db)):
    statement = (
        select(Diagnosis)
        .join(Animal)
        .where(Animal.user_id == id)
    )
    history_table = db.exec(statement).all()
    return history_table

@router.delete("/reports/delete")
async def delete_diagnosis(request: DiagnosisDeleteRequest, db: Session = Depends(get_db)):
    diagnosis = db.exec(select(Diagnosis).where(Diagnosis.id.in_(request.diagnosis_ids))).all()

    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis report not found")

    for record in diagnosis:
        db.delete(record)

    db.commit()
    remaining_diagnoses = db.exec(select(Diagnosis)).all()
    return remaining_diagnoses
