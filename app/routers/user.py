from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import Hash, allow_admin, allow_teacher, allow_student
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserResponse, Token
from app.token import create_access_token, get_current_user

router = APIRouter(tags=["user"])

CurrentUser = Annotated[UserModel, Depends(get_current_user)]


@router.post("/create-user", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="A user with this email already exists")

    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=Hash.hash_password(data.password),
        role=data.role.value,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    if not user or not Hash.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser):
    return current_user


@router.get("/users", response_model=list[UserResponse])
def get_all_users(current_user: CurrentUser, db: Session = Depends(get_db)):
    allow_admin(current_user)
    return db.query(UserModel).all()


@router.get("/teacher/dashboard")
def teacher_dashboard(current_user: CurrentUser):
    allow_teacher(current_user)
    return {"message": f"Welcome teacher {current_user.name}", "role": current_user.role}


@router.get("/student/dashboard")
def student_dashboard(current_user: CurrentUser):
    allow_student(current_user)
    return {"message": f"Welcome student {current_user.name}", "role": current_user.role}