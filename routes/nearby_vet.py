from fastapi import APIRouter, Query
from typing import List
from schemas import VetStore
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@router.get("/nearbyvet", response_model=List[VetStore])
async def get_nearest_vet_stores(lat: float = Query(...), lon: float = Query(...)):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": 10000,  # Search within 5km
        "type": "veterinary_care",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data:
        vet_stores = [
            {
                "name": store["name"],
                "address": store.get("vicinity", "No address"),
                "latitude": store["geometry"]["location"]["lat"],
                "longitude": store["geometry"]["location"]["lng"]
            }
            for store in data["results"]
        ]
        return vet_stores

    return {"message": "No vet stores found"}
