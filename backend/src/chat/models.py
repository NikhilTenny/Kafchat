from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Session, Relationship, select
from typing import Optional
from pydantic import BaseModel
from src.authentication.models import User
from src.chat.schemas import SendMessage


class Messages(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    body: str = Field(max_length=1000, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    sender_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    conv_id: int = Field(foreign_key="conversation.id", nullable=False, index=True)


class Conversation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    is_group: bool = Field(default=False)  


class ConversationParticipants(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    conv_id: int = Field(foreign_key="conversation.id", nullable=False, index=True)







