from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_diagnosis_endpoint():
    """Test the diagnosis model API endpoint"""
    request_data = {
        "species": "dog",
        "breed": "bulldog",
        "gender": "male",
        "symptoms": ["coughing", "loss of appetite","Nasal discharge"],
        "follow_up": {
            "Appetite_Loss": True,
            "Vomiting": False,
            "Diarrhea": False,
            "Coughing": True,
            "Labored_Breathing": False,
            "Lameness": False,
            "Skin_Lesions": False,
            "Nasal_Discharge": True,
            "Eye_Discharge": False
        }
    }
    response = client.post("/diagnosis/model", json=request_data)
    assert response.status_code == 200  # Expecting a successful response
    data = response.json()
    assert "prioritized_results" in data
    assert isinstance(data["prioritized_results"], dict)

def test_invalid_species():
    """Test with an invalid species"""
    request_data = {
        "species": "dragon",
        "breed": "Nightfury",
        "gender": "male",
        "symptoms": ["vomiting","loss of appetite"],
        "follow_up": {
            "Appetite_Loss": True,
            "Vomiting": True,
            "Diarrhea": False,
            "Coughing": False,
            "Labored_Breathing": False,
            "Lameness": False,
            "Skin_Lesions": False,
            "Nasal_Discharge": True,
            "Eye_Discharge": False}
    }

    response = client.post("/diagnosis/model", json=request_data)
    assert response.status_code == 400  # Expecting a bad request

def test_missing_field():
    """Test request with missing required fields"""
    request_data = {
        "breed": "persian",
        "gender": "male",
        "symptoms": ["vomiting","fever"]
    }

    response = client.post("/diagnosis/model", json=request_data)
    assert response.status_code == 422  # Expecting validation error


