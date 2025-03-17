from fastapi import APIRouter, HTTPException
from schemas import DiagnosisRequest, DiagnosisResponse
from services.animal_disease_prediction import AnimalSymptoms
import logging
import traceback
logging.basicConfig(level=logging.ERROR)

router = APIRouter()
@router.post("/model", response_model=DiagnosisResponse)
async def generate_diagnosis(request: DiagnosisRequest):
    try:
        if not all([request.species, request.breed, request.gender]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        if len(request.symptoms) < 2:
            raise HTTPException(status_code=400, detail="At least 2 symptoms required")
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
        diagnosis_engine.assign_treatment()
        diagnosis_engine.assign_description()

        return DiagnosisResponse(
            #prognosis=diagnosis_engine.prognosis,
            prioritized_results= diagnosis_engine.prioritized_results
        )
    except KeyError as e:
        logging.error(f"Invalid species provided: {str(e)}")
        print("Invalid species provided:", str(e))
        raise HTTPException(status_code=400, detail="Invalid species provided.")

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        print("Error processing request:",str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))