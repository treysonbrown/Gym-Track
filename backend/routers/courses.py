from operator import countOf
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from sqlmodel import Session, Table, func, select

from database import get_db
from models import Course, Member, Trainer
from schemas import CreateCourseReqeust, UpdateCourseRequest

router = APIRouter()



### GET ###
@router.get("/courses")
async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    return db.exec(select(Course)).all()


@router.get("/courses/{course_id}")
async def get_course_attendance(course_id: int, db: Session = Depends(get_db)) -> int:
    attendance: list[Member] | None = None
    course: Course | None = None
    course = db.exec(select(Course).where(Course.id == course_id)).first()

    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with the id {course_id} was not found") 

    attendance = course.members
    if attendance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return len(attendance)

@router.get("/courses/day")
async def get_day_of_week(db: Session = Depends(get_db)):
    func.count()




### POST ###
@router.post("/courses", status_code=status.HTTP_202_ACCEPTED)
async def create_course(create_course_request: CreateCourseReqeust, db: Session = Depends(get_db)) -> int:
    trainer: Trainer | None = None
    trainers: list[Trainer] = db.exec(select(Trainer)).all()

    for t in trainers:
        if create_course_request.trainer_id == t.id:
            trainer = t

    if trainer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trainer with the id {create_course_request.trainer_id} was not found")



    course: Course = Course(**create_course_request.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)

    assert course.id is not None
    return course.id


@router.post("/courses/{course_id}/members/{member_id}", status_code=status.HTTP_201_CREATED)
def add_course_attendance(member_id: int, course_id: int, db: Session = Depends(get_db)) -> Member:
    member: Member | None = None
    member = db.get(Member, member_id)
    if member == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with the id {id} was not found")
    course: Course | None = None
    course = db.get(Course, course_id)
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with the id {id} was not found")

    course.members.append(member)

    db.add(course)
    db.commit()
    db.refresh(course)
    return course.members[-1]



### PATCH ###
@router.patch('/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def patch_member(course_id: int, update_fields: UpdateCourseRequest, db: Session = Depends(get_db)):
    course: Course | None = db.get(Course, course_id)
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with the id {id} was not found")

    for k, v in update_fields.model_dump(exclude_unset=True).items():
        setattr(course, k, v)

    db.commit()


### DELETE ###

@router.delete("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, db: Session = Depends(get_db)) -> None:
    courses: list[Course] = db.exec(select(Course)).all()
    course: Course | None = None
    for c in courses:
        if id == c.id:
            course = c
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(course)
    db.commit()


