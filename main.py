from fastapi import FastAPI

from app.database import Base, engine
from app.routers import user

app = FastAPI(title="Teacher-Student Management System")

app.include_router(user.router)

Base.metadata.create_all(bind=engine)
