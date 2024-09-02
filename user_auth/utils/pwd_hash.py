from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pass_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(default_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(default_password, hashed_password)