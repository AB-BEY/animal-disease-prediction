from fastapi import APIRouter, HTTPException
from schemas import DiagnosisRequest, DiagnosisResponse
from services.animal_disease_prediction import AnimalSymptoms
import logging
logging.basicConfig(level=logging.ERROR)

router = APIRouter()
@router.post("/model", response_model=DiagnosisResponse)
async def generate_diagnosis(request: DiagnosisRequest):
    try:
        # Create an instance of AnimalSymptoms with the provided parameters.
        diagnosis_engine = AnimalSymptoms(
            species=request.species,
            breed=request.breed,
            gender=request.gender,
            symptoms=request.symptoms,
            **request.follow_up  # Unpack follow-up responses if any.
        )

        diagnosis_engine.priority_one()
        diagnosis_engine.priority_two()
        diagnosis_engine.priority_three()

        return DiagnosisResponse(
            #prognosis=diagnosis_engine.prognosis,
            prioritized_results= diagnosis_engine.prioritized_results
        )
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))