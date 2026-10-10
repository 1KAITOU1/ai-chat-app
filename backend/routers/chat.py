from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from datetime import datetime, timezone
from schemas.chat import ChatRequest
from services.llm_service import stream_chat
from db import Conversation, Message, get_session, engine

router = APIRouter(prefix="/api/chat", tags=["Chat"])

def now_utc():
    return datetime.now(timezone.utc)

@router.post("/stream")
async def chat_stream(request: ChatRequest, session: Session = Depends(get_session)):
    conv_id = request.conversation_id
    if not conv_id:
        raise HTTPException(status_code=400, detail="conversation_id is required")

    conv = session.get(Conversation, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = request.messages[-1].content

    history_stmt = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at)
    history = session.exec(history_stmt).all()

    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": user_message})

    session.add(Message(conversation_id=conv_id, role="user", content=user_message))

    if len(history) == 0:
        conv.title = user_message[:30]

    conv.updated_at = now_utc()
    session.add(conv)
    session.commit()

    async def event_generator():
        full_reply = ""
        async for chunk in stream_chat(messages, request.model):
            full_reply += chunk
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

        with Session(engine) as s:
            s.add(Message(conversation_id=conv_id, role="assistant", content=full_reply))
            conv2 = s.get(Conversation, conv_id)
            if conv2:
                conv2.updated_at = now_utc()
                s.add(conv2)
            s.commit()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
