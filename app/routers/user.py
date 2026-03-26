from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.dependencies import (
    Hash,
    allow_admin,
    allow_teacher,
    allow_student,
)
from app.models.user import User as UserModel
from app.models.profiles import TeacherProfile, StudentProfile
from app.models.class_room import Class as ClassModel
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
    ChangeUserPasswordRequest
)
from app.token import (
    create_access_token,
    get_current_user
)

router = APIRouter(tags=["user"])

CurrentUser = Annotated[UserModel, Depends(get_current_user)]


@router.post(
    "/create-user",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db),
):
    try:
        # Check if user already exists
        existing_user = db.query(UserModel).filter(
            UserModel.email == data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists",
            )

        # Create user
        new_user = UserModel(
            name=data.name,
            email=data.email,
            password=Hash.hash_password(data.password),
            role=data.role if isinstance(data.role, str) else data.role.value,
        )

        db.add(new_user)
        db.flush()  # gets ID without committing

        # Create role-specific profile
        if data.role == "teacher":
            profile = TeacherProfile(
                user_id=new_user.id,
                salary=data.salary
            )
            db.add(profile)

        elif data.role == "student":
            profile = StudentProfile(
                user_id=new_user.id,
                dues=data.dues,
            )
            db.add(profile)

        # Commit everything together
        db.commit()
        db.refresh(new_user)

        return new_user

    except HTTPException:
        # Let FastAPI handle known errors
        db.rollback()
        raise

    except Exception as e:
        # Rollback on any unexpected error
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(
        UserModel.email == data.username
    ).first()
    if not user or not Hash.verify_password(
            data.password, user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser):
    return current_user


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
        current_user: CurrentUser,
        db: Session = Depends(get_db),
):
    allow_admin(current_user)
    return db.query(UserModel).all()


@router.put("/users/change_password")
def change_user_password(
        current_user: CurrentUser,
        data: ChangeUserPasswordRequest,
        db: Session = Depends(get_db),
):
    old_password = data.old_password
    new_password = data.new_password
    if not Hash.verify_password(old_password, current_user.password):
        raise HTTPException(
            status_code=401,
            detail='Invalid password'
        )
    if Hash.verify_password(
            data.new_password,
            current_user.password
    ):
        raise HTTPException(
            status_code=200,
            detail="New password must be different"
        )
    user = db.query(UserModel).filter(
        UserModel.email == current_user.email
    ).first()
    user.password = Hash.hash_password(new_password)
    db.commit()
    return {'message': 'Password changed'}


@router.get("/teacher/dashboard")
def teacher_dashboard(
        current_user: CurrentUser,
        db: Session = Depends(get_db),
):
    allow_teacher(current_user)

    stmt = (
        select(UserModel)
        .where(UserModel.id == current_user.id)
        .options(
            selectinload(UserModel.teacher_profile),
        )
    )
    user = db.execute(stmt).scalars().first()

    # Fetch classes taught by this teacher with enrolled students eager-loaded
    classes_stmt = (
        select(ClassModel)
        .where(ClassModel.teacher_id == current_user.id)
        .options(
            selectinload(ClassModel.students),
        )
    )
    classes = db.execute(classes_stmt).scalars().all()

    profile = user.teacher_profile[0] if user.teacher_profile else None

    classes_data = []
    for c in classes:
        students_list = [
            {
                "id": str(s.id),
                "name": s.name,
                "email": s.email,
            }
            for s in c.students
        ]
        classes_data.append({
            "id": str(c.id),
            "name": c.name,
            "subject": c.subject,
            "students": students_list,
        })

    return {
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
        "profile": {
            "salary": profile.salary if profile else None,
            "is_active": profile.is_active if profile else None,
        },
        "classes": classes_data,
    }


@router.get("/student/dashboard")
def student_dashboard(
        current_user: CurrentUser,
        db: Session = Depends(get_db),
):
    allow_student(current_user)

    # Eager-load the student's profile and their enrolled classes,
    # and for each class load the teacher (User).
    stmt = (
        select(UserModel)
        .where(UserModel.id == current_user.id)
        .options(
            selectinload(UserModel.student_profile),
            selectinload(UserModel.classes).selectinload(ClassModel.teacher),
        )
    )
    user = db.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = user.student_profile[0] if user.student_profile else None

    classes_data = []
    for c in user.classes:
        teacher = c.teacher
        classes_data.append({
            "id": str(c.id),
            "name": c.name,
            "subject": c.subject,
            "teacher": {
                "id": str(teacher.id) if teacher else None,
                "name": teacher.name if teacher else None,
                "email": teacher.email if teacher else None,
            },
        })

    return {
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
        "profile": {
            "dues": profile.dues if profile else None,
            "pending_dues": profile.pending_dues if profile else None,
            "is_active": profile.is_active if profile else None,
        },
        "classes": classes_data,
    }
