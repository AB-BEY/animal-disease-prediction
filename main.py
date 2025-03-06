from fastapi import FastAPI, Response
from database import create_tables
from routes import auth, detect, add_pet, history_report, diagnosis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "https://vet-vista-am5q.onrender.com",
    "https://vet-vista.onrender.com",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manually handle OPTIONS requests (CORS preflight requests)
@app.options("/{full_path:path}")
async def preflight_request(full_path: str):
    response = JSONResponse(content={"message": "Preflight request handled"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(detect.router, prefix="/detect", tags=["Detection"])
app.include_router(add_pet.router, prefix="/mypets", tags=["My Pets"])
app.include_router(history_report.router, prefix="/history", tags=["History"])
app.include_router(diagnosis.router, prefix="/diagnosis", tags=["Diagnosis"])


@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "Welcome to the Animal Disease Prediction System!"}

# Create tables on startup
@app.on_event("startup")
def on_startup():
    # delete_tables()  # Uncomment to delete tables
    create_tables()
    print("Tables created successfully")

