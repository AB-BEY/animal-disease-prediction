from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Animal, User
from schemas import AnimalCreate, AllPetResponse, AnimalResponse


router = APIRouter()

@router.post("/addpet", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    existing_animal = db.exec(select(Animal).where(Animal.animal_name == animal.animal_name)).first()
    if existing_animal:
        raise HTTPException(status_code=400, detail="Pet already registered")

    new_animal = Animal(animal_name=animal.animal_name, age=animal.age, species=animal.species, breed=animal.breed, user_id=animal.user_id)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return new_animal

@router.get("/allpets/{id}", response_model=list[AllPetResponse])
async def get_all_pets(id: int, db: Session = Depends(get_db)):
    all_pets = db.exec(select(Animal).where(Animal.user_id == id)).all()
    if not all_pets:
        return{"response":"This user has no pet"}

    return all_pets
