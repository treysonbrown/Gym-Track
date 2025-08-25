from sqlmodel import Date, Field, Relationship, SQLModel, Time, false, table


class MemberClassLink(SQLModel, table=True):
    member_id: int  | None = Field(foreign_key="member.id", primary_key=True)
    course_id: int  | None = Field(foreign_key="course.id", primary_key=True)

class Member(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    active: bool | None = True
    courses: list["Course"] = Relationship(back_populates="members", link_model=MemberClassLink)

class Trainer(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    specialty: str
    courses: list["Course"] = Relationship(back_populates="trainer")

class Course(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    trainer_id: int = Field(foreign_key="trainer.id")
    date: str
    duration: str
    trainer: Trainer = Relationship(back_populates="courses")
    members: list[Member] = Relationship(back_populates="courses", link_model=MemberClassLink)



