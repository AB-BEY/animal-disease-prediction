from fastapi import FastAPI, Depends, HTTPException, status
from database import create_tables
from routes import auth, detect

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(detect.router, prefix="/detect", tags=["Detection"])


# Create tables on startup
@app.on_event("startup")
def on_startup():
    # delete_tables()  # Uncomment to delete tables
    create_tables()
    print("Tables created successfully")

