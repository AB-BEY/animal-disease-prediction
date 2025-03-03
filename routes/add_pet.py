from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Animal
from schemas import AnimalCreate, AnimalResponse, AllPetResponse

router = APIRouter()

@router.post("/addpet", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    existing_animal = db.exec(select(Animal).where(Animal.animal_name == animal.animal_name)).first()
    if existing_animal:
        raise HTTPException(status_code=400, detail="Pet already registered")

    new_animal = Animal(name=animal.animal_name, age=animal.age, specie=animal.species, breed=animal.breed)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return new_animal

@router.get("/addpet/{user_id}", response_model=list[AllPetResponse])
async def get_all_pets(user_id: int,db: Session = Depends(get_db)):
    all_pets = db.exec(select(Animal).where(Animal.user_id == user_id)).all()
    return all_pets