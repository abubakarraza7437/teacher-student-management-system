from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead
from app.dependencies import hash_password
router = APIRouter(
    tags=["user"],
)

@router.post("/user")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("/create-user", response_model=UserRead)
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
    hashed_password = hash_password(data.password)
    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=hashed_password,
        role=data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user