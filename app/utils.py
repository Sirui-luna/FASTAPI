#type of encryption method we will use
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#encrypt password: hashing with bcrypt
def hash(password: str):
    return pwd_context.hash(password)

#check if the password matches
def verify(plain_password,hashed_passwrod):
    return pwd_context.verify(plain_password, hashed_passwrod)