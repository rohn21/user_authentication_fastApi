"""
    This file contains following functionality
    1. Convert user entered password into hashed password that will to increase password security
    2. Verifies the actual defined/choosen password by user with stored hashed password
        - will check both password and return the appropriate result in Boolean data_type
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to convert a password into hashed password
def pass_hash(password:str) -> str:
    return pwd_context.hash(password)

# function to verify both default_password and hashed password are same or not
def verify_password(default_password: str, hashed_password: str) -> bool:   # return in boolean data_type
    return pwd_context.verify(default_password, hashed_password)