from sqlmodel import create_engine, SQLModel, Session
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10,
        "ssl_disabled": False  # Set True if not using SSL
    }
)

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
