from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from decimal import Decimal

# User Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str

    # Relationship with Animal
    animals: List["Animal"] = Relationship(back_populates="user")


# Animal Model
class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_name: str = Field(max_length=100, nullable=False)
    breed: str = Field(max_length=100, nullable=False)
    age: int = Field(nullable=False)
    species: str = Field(max_length=100, nullable=False)

    # Foreign Key to User
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Relationships
    user: Optional[User] = Relationship(back_populates="animals")
    diagnoses: List["Diagnosis"] = Relationship(back_populates="animal", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


# Diagnosis Model
class Diagnosis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    diagnosis_description: str = Field(max_length=250, nullable=False)
    confidence_level: Decimal = Field(max_digits=5, decimal_places=2, nullable=False)
    diagnosis_date: date = Field(nullable=False)

    # Foreign Key to Animal
    animal_id: Optional[int] = Field(default=None, foreign_key="animal.id")

    # Relationships
    animal: Optional[Animal] = Relationship(back_populates="diagnoses")
    treatments: List["Treatment"] = Relationship(back_populates="diagnosis", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


# Treatment Model
class Treatment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recommended_treatment: str = Field(max_length=250, nullable=False)

    # Foreign Key to Diagnosis
    diagnosis_id: Optional[int] = Field(default=None, foreign_key="diagnosis.id")

    # Relationship
    diagnosis: Optional[Diagnosis] = Relationship(back_populates="treatments")

class PasswordResetToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    token: str = Field(index=True, unique=True)
    expires_at: datetime
    used: bool = Field(default=False)