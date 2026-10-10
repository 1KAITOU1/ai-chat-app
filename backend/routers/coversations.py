from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import Conversation, Message, get_session

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("")
def list_conversations(session: Session = Depends(get_session)):
    return session.exec(select(Conversation).order_by(Conversation.created_at.desc())).all()

@router.post("")
def create_conversation(session: Session = Depends(get_session)):
    conv = Conversation(title="新对话")
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv

@router.get("/{conv_id}/messages")
def get_messages(conv_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Message).where(Message.conversation_id == conv_id)).all()

@router.delete("/{conv_id}")
def delete_conversation(conv_id: int, session: Session = Depends(get_session)):
    session.exec(select(Message).where(Message.conversation_id == conv_id))
    # 实际用 delete 语句
    session.delete(session.get(Conversation, conv_id))
    session.commit()
    return {"ok": True}