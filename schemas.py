from pydantic import BaseModel, EmailStr
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

class UserInDB(UserCreate):
    hashed_password: str

class AnimalCreate(BaseModel):
    name: str
    age: str
    species: str
    breed: str

class AnimalResponse(BaseModel):
    id: int
    name: str
    age: str
    species: str
    breed: str

