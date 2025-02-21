from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from src.config import sqlite_file_name, sqlite_url


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def consume_session() -> Session:
    return Session(engine)





session_dep = Annotated[Session, Depends(get_session)]