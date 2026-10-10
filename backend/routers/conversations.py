from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, delete
from datetime import datetime
from db import Conversation, Message, get_session

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("")
def list_conversations(session: Session = Depends(get_session)):
    stmt = select(Conversation).order_by(Conversation.updated_at.desc())
    return session.exec(stmt).all()

@router.post("")
def create_conversation(session: Session = Depends(get_session)):
    conv = Conversation(title="新对话")
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv

@router.get("/{conv_id}")
def get_conversation(conv_id: int, session: Session = Depends(get_session)):
    conv = session.get(Conversation, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.get("/{conv_id}/messages")
def get_messages(conv_id: int, session: Session = Depends(get_session)):
    stmt = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at)
    return session.exec(stmt).all()

@router.delete("/{conv_id}")
def delete_conversation(conv_id: int, session: Session = Depends(get_session)):
    conv = session.get(Conversation, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    session.exec(delete(Message).where(Message.conversation_id == conv_id))
    session.delete(conv)
    session.commit()
    return {"ok": True}
