from pydantic import BaseModel, EmailStr
from datetime import date
from decimal import Decimal
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # Plaintext password for input

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Enables ORM mode

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    id: int
    name: str
    email: EmailStr

class UserInDB(UserCreate):
    hashed_password: str

class AnimalCreate(BaseModel):
    animal_name: str
    age: int
    species: str
    breed: str

class AnimalResponse(BaseModel):
    animal_name: str
    age: int
    species: str
    breed: str

class HistoryResponse(BaseModel):
    animal_id: int
    diagnosis_description: str
    confidence_level: Decimal
    diagnosis_date: date

class AllPetResponse(BaseModel):
    animal_name: str
    species: str
    age: int
    breed: str



