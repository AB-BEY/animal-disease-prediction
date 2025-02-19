from fastapi import APIRouter

router = APIRouter()

@router.post("/detect/fg")  # Updated path to avoid conflict
def get_detect():
    return {"message": "Hello Detect"}
