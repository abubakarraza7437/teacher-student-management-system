from fastapi import HTTPException, status
from passlib.context import CryptContext
import string
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user) -> None:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )


allow_admin = RoleChecker(["admin"])
allow_teacher = RoleChecker(["admin", "teacher"])
allow_student = RoleChecker(["admin", "student"])


class HandlePassword:

    @staticmethod
    def generate_password(length: int = 12):
        if length < 4:
            raise ValueError("Password length must be at least 4")

        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation),
        ]

        all_chars = string.ascii_letters + string.digits + string.punctuation

        password += [secrets.choice(all_chars) for _ in range(length - 4)]

        secrets.SystemRandom().shuffle(password)

        return ''.join(password)
