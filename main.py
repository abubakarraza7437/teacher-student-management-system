from fastapi import FastAPI

# from app.database import Base, engine
from app.routers import user, class_room


app = FastAPI(title="Teacher-Student Management System")

app.include_router(user.router)
app.include_router(class_room.router)

# Base.metadata.create_all(bind=engine)
