

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import get_db
from models import Trainer
from schemas import CreateTrainerRequest, UpdateTrainerRequest


router = APIRouter()

### GET ###

@router.get("/trainers")
async def get_trainers(db: Session = Depends(get_db)) -> list[Trainer]:
    return db.exec(select(Trainer)).all()


### POST ###

@router.post("/trainers", status_code=status.HTTP_202_ACCEPTED)
async def create_trainer(create_trainer_request: CreateTrainerRequest, db: Session = Depends(get_db)) -> int:
    trainer: Trainer = Trainer(name=create_trainer_request.name, specialty=create_trainer_request.speciality)
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    assert trainer.id is not None
    return trainer.id


### PATCH ###
@router.patch('/trainers/{trainer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def patch_member(trainer_id: int, update_fields: UpdateTrainerRequest, db: Session = Depends(get_db)):
    trainer: Trainer | None = db.get(Trainer, trainer_id)
    if trainer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trainer with the id {id} was not found")

    for k, v in update_fields.model_dump(exclude_unset=True).items():
        setattr(trainer, k, v)

    db.commit()

### DELETE ###


@router.delete("/trainers/{trainer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trainer(trainer_id: int, db: Session = Depends(get_db)) -> None:
    trainer: Trainer | None = db.get(Trainer, trainer_id)
    if trainer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(trainer)
    db.commit()
