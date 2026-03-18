from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import allow_teacher
from app.models.class_room import Class
from app.models.user import User
from app.schemas.class_room import CreateClass, AddStudent, ReadStudent
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

    class_room = db.query(Class).filter(
        Class.name == data.class_name,
        Class.teacher_id == current_user.id,
    ).first()
    if not class_room:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    not_found = []
    added = []
    for email in data.emails:
        student = db.query(User).filter(
            User.email == email,
            User.role == "student",
        ).first()
        if not student:
            not_found.append(email)
            continue
        if student not in class_room.students:
            class_room.students.append(student)
            added.append(email)

    db.commit()

    result = {"added": added}
    if not_found:
        result["not_found"] = not_found
    return result


@router.get("/student")
def get_students(
        current_user: CurrentUser,
        data: ReadStudent,
        db: Session = Depends(get_db),
        ):

    allow_teacher(current_user)
    students = db.query(Class).filter(Class.name == data.class_name).all()
    return students
