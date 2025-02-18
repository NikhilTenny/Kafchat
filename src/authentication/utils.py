from passlib.context import CryptContext
from src.database import session_dep
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from src.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import FastAPI, Request, HTTPException, status




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    """Generates a JWT access token with an expiration time.

    Args:
        data (dict): The payload data to encode in the token (e.g., user details).
        expire_delta (timedelta | None, optional): The time duration until the token expires.
            Defaults to `ACCESS_TOKEN_EXPIRE_MINUTES` if not provided.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if not expire_delta:
        expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def extract_user_from_token(access_token: str):
    return jwt.decode(access_token, key=SECRET_KEY, algorithms=ALGORITHM)

def extract_user(request: Request):
    auth_header = request._headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        access_token = auth_header.replace("Bearer ", "")
        user = extract_user_from_token(access_token)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


def get_current_user(request: Request):
    return extract_user(request)

    


