from passlib.context import CryptContext

def hash_password(password):
    pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pass_context.hash(password)
