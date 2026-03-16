from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/create-user", response_model=UserRead)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = (db.query(UserModel).
                     filter(UserModel.email == data.email).
                     first())
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=data.password,
        role=data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
