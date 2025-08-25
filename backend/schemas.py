from pydantic import BaseModel

from models import Course


class CreateMemberRequest(BaseModel):
    name: str


class CreateTrainerRequest(BaseModel):
    name: str
    speciality: str

class CreateCourseReqeust(BaseModel):
    trainer_id: int
    name: str
    duration: str
    date: str

class CoursePopularityReturn(BaseModel):
    date: str

class UpdateMemberRequest(BaseModel):
    name: str | None = None
    active: bool | None = None
    courses: list[Course] | None  = None 

class UpdateTrainerRequest(BaseModel):
    name: str | None = None
    specialty: str | None = None
    courses: list["Course"] | None = None


class UpdateCourseRequest(BaseModel):
    name: str | None = None
    trainer_id: int | None = None
    date: str | None = None
    duration: str | None = None
    trainer_id: int | None = None
