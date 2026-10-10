from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.chat import ChatRequest
from services.llm_service import stream_chat

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    async def event_generator():
        async for chunk in stream_chat(messages, request.model):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
