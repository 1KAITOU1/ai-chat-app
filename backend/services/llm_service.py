import json
import httpx
from core.config import settings

async def stream_chat(messages: list[dict], model: str = None):
    """调用 Ollama 流式对话接口，逐块 yield 内容"""
    model = model or settings.DEFAULT_MODEL
    url = f"{settings.OLLAMA_BASE_URL}/api/chat"

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST", url,
            json={"model": model, "messages": messages, "stream": True}
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
                    if data.get("done", False):
                        break
