import asyncio
import json
from typing import Any, Dict, Tuple

import httpx

from .prompts import image_prompt, text_system_prompt
from .settings import settings


HEADERS = {
    "Authorization": f"Bearer {settings.openrouter_api_key}",
    "HTTP-Referer": "https://tohu-kaiako.example",
    "X-Title": "Tohu Kaiako",
}

if not settings.openrouter_api_key:
    HEADERS.pop("Authorization")


async def call_text(theme: str, level: str, keywords: str) -> Dict[str, Any]:
    payload = {
        "model": settings.text_model,
        "messages": [
            {"role": "system", "content": text_system_prompt(theme, level, keywords)}
        ],
        "temperature": 0.3,
    }
    async with httpx.AsyncClient(timeout=settings.timeout_secs) as client:
        response = await client.post(
            f"{settings.openrouter_base_url}/chat/completions",
            headers=HEADERS,
            json=payload,
        )
        response.raise_for_status()
        try:
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("Invalid text generation response") from exc


async def call_image(theme: str, keywords: str) -> str:
    payload = {
        "model": settings.image_model,
        "prompt": image_prompt(theme, keywords),
    }
    async with httpx.AsyncClient(timeout=settings.timeout_secs) as client:
        response = await client.post(
            f"{settings.openrouter_base_url}/images",
            headers=HEADERS,
            json=payload,
        )
        response.raise_for_status()
        try:
            data = response.json()["data"][0]["url"]
            return data
        except (KeyError, IndexError, ValueError) as exc:
            raise RuntimeError("Invalid image generation response") from exc


async def generate_pack(theme: str, level: str, keywords: str) -> Tuple[Dict[str, Any], str]:
    text_task = asyncio.create_task(call_text(theme, level, keywords))
    image_task = asyncio.create_task(call_image(theme, keywords or ""))

    text_json, image_url = await asyncio.gather(text_task, image_task)
    return text_json, image_url
