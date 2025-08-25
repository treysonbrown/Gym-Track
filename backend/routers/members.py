from typing import Counter, Sequence
from fastapi import Depends, FastAPI, APIRouter, HTTPException, UploadFile, File, status
from sqlmodel import Session, select

from database import get_db
from models import Course, Member
from schemas import CreateMemberRequest, UpdateMemberRequest

router = APIRouter()


### GET ###

@router.get("/members")
async def get_members(db: Session = Depends(get_db)) -> list[Member] | Sequence[Member]:
    return db.exec(select(Member)).all()

@router.get("/members/active")
async def get_active_members(db: Session = Depends(get_db)) -> list[Member]:
    return db.exec(select(Member).where(Member.active == True))




### POST ###

@router.post("/members", status_code=status.HTTP_201_CREATED)
async def create_member(create_member_request: CreateMemberRequest, db: Session = Depends(get_db)) -> int:
    member: Member = Member(name=create_member_request.name)
    db.add(member)
    db.commit()
    db.refresh(member)

    assert member.id is not None
    return member.id







### PATCH ###
@router.patch('/members/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def patch_member(member_id: int, update_fields: UpdateMemberRequest, db: Session = Depends(get_db)):
    member: Member | None = db.get(Member, member_id)
    if member == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with the id {id} was not found")


    for k, v in update_fields.model_dump(exclude_unset=True).items():
        setattr(member, k, v)

    db.commit()








### DELETE ###
@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: int, db: Session = Depends(get_db)) -> None:

    member: Member | None = db.get(Member, member_id)

    if member == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with the id {id} was not found")

    db.delete(member)
    db.commit()








