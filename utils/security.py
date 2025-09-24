from passlib.context import CryptContext 
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")
access_token_expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + (timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, secret_key, algorithm = algorithm)

