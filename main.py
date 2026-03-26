from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.database import Base, engine
from app.routers import user, class_room


app = FastAPI(title="Teacher-Student Management System")

# Allow the Next.js frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(class_room.router)

# Base.metadata.create_all(bind=engine)
