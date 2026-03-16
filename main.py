from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead
from passlib.context import CryptContext


app = FastAPI()

Base.metadata.create_all(bind=engine)

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
    hashed_password = pass_context.hash(data.password)
    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=hashed_password,
        role=data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
