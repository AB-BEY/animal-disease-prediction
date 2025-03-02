from fastapi import FastAPI
from database import create_tables
from routes import auth, detect, add_pet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://vet-vista-am5q.onrender.com",
    "https://vet-vista.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(detect.router, prefix="/detect", tags=["Detection"])
app.include_router(add_pet.router, prefix="/addpet", tags=["Add Pet"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Animal Disease Prediction System!"}

# Create tables on startup
@app.on_event("startup")
def on_startup():
    # delete_tables()  # Uncomment to delete tables
    create_tables()
    print("Tables created successfully")

