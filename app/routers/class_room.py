from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import allow_teacher
from app.models.class_room import Class
from app.models.user import User
from app.schemas.class_room import CreateClass, AddStudent
from app.token import get_current_user

router = APIRouter(tags=["class"])

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/create-class", status_code=201)
def create_class(
    data: CreateClass,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    allow_teacher(current_user)

    teacher = db.query(User).filter(
        User.email == data.email,
        User.role == "teacher",
    ).first()
    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    class_room = Class(
        name=data.name,
        subject=data.subject,
        teacher_id=current_user.id,
    )
    db.add(class_room)
    db.commit()
    db.refresh(class_room)
    return class_room


@router.get("/class")
def get_classes(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return db.query(Class).filter(
        Class.teacher_id == current_user.id
    ).all()


@router.post("/add-student")
def add_students(
    data: AddStudent,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    allow_teacher(current_user)

    # TODO: implement add-student logic
    pass
