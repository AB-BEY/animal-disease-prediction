from sqlmodel import create_engine, SQLModel, Session
from config import settings

# Create the database engine
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

# Function to get a database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Create tables (if they don't exist)
def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_tables():
    SQLModel.metadata.drop_all(engine)
