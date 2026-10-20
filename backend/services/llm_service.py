import json
import httpx
from core.config import settings

async def stream_chat(messages: list[dict], model: str = None):
    model = model or settings.DEFAULT_MODEL
    url = f"{settings.OLLAMA_BASE_URL}/api/chat"

    async with httpx.AsyncClient(timeout=300.0) as client:
        async with client.stream(
            "POST", url,
            json={"model": model, "messages": messages, "stream": True}
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    data = json.loads(line)
                    if "message" in data:
                        # 提取思考内容（如果有）
                        thinking = data["message"].get("thinking", "")
                        if thinking:
                            yield f"*[思考中]* {thinking}\n"
                        
                        # 提取最终内容
                        content = data["message"].get("content", "")
                        if content:
                            yield content
                            
                    if data.get("done", False):
                        break