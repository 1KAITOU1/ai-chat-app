from sqlmodel import SQLModel, Field, Session, create_engine
from datetime import datetime, timezone
from typing import Optional

engine = create_engine(
    "sqlite:///./data.db",
    connect_args={"check_same_thread": False}
)

def now_utc():
    return datetime.now(timezone.utc)

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = "新对话"
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str
    content: str
    created_at: datetime = Field(default_factory=now_utc)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
