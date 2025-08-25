from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import courses, members, trainers


app = FastAPI(title="Gym", version="0.1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members.router, tags=["Members"])
app.include_router(trainers.router, tags=["Trainers"])
app.include_router(courses.router, tags=["Course"])

