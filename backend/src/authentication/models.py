from datetime import datetime, timezone
from fastapi import Depends
from sqlmodel import Field, SQLModel, Session, select
from pydantic import BaseModel
from src.database import session_dep
from src.authentication.utils import verify_password
from typing import List, Union


class UserBase(SQLModel):
    first_name: str = Field(max_length=40, nullable=False)
    last_name: str = Field(max_length=40, nullable=False)
    user_name: str = Field(nullable=False, unique=True, max_length=40, min_length=4)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    # documents: List['Document'] = Relationship(back_populates="user")

class UserPublic(UserBase):
    id: int = Field(default=None, primary_key=True)
    is_active: bool = Field(default=False)

class UserCreate(UserBase):
    password: str = Field(nullable=False)


class UserLogin(BaseModel):
    user_name: str
    password: str


def get_user(session: Session, username):
    return session.query(User).filter(User.user_name== username).first()


def get_user_by_id(session: Session, user_id):
    return session.exec(select(User).filter(User.id == user_id)).first()

def authenticate_user(session: Session, username: str, password: str):
    user = get_user(session,username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def check_if_user_exists(user_name: str, session: session_dep) -> bool: 
    """
        Checks if a user with the given username exists in the database.
    """
    user_exists = session.query(User).filter(User.user_name==user_name).first()
    return user_exists is not None

def logout_user(user_name: str, session: session_dep) -> bool:
    if user := check_if_user_exists(user_name, session):
        pass

def list_users(session, current_user: Union[User,None] = None, ):
    try:
        users = session.exec(
            select(User).filter(User.id != current_user["id"])
        ).all()
        return users
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")   





    






