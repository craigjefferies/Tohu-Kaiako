import asyncio
import json
import logging
from typing import Any, Dict, Tuple

import httpx

from .prompts import image_prompt, text_system_prompt
from .settings import settings

logger = logging.getLogger("tohu-kaiako")

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
    logger.info(f"Calling OpenRouter with model: {settings.text_model}")
    logger.info(f"API Key present: {bool(settings.openrouter_api_key)}")
    logger.info(f"Headers: {list(HEADERS.keys())}")
    
    async with httpx.AsyncClient(timeout=settings.timeout_secs) as client:
        response = await client.post(
            f"{settings.openrouter_base_url}/chat/completions",
            headers=HEADERS,
            json=payload,
        )
        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"OpenRouter error: {error_detail}")
            raise RuntimeError(f"OpenRouter API error ({response.status_code}): {error_detail}")
        response.raise_for_status()
        try:
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]
            
            # Strip markdown code blocks if present
            content = content.strip()
            if content.startswith("```"):
                # Remove opening ```json or ```
                lines = content.split("\n")
                lines = lines[1:]  # Remove first line with ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]  # Remove last line with ```
                content = "\n".join(lines)
            
            logger.info(f"Stripped content to parse: {content[:300]}...")
            return json.loads(content)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            logger.error(f"Failed to parse response: {exc}")
            logger.error(f"Content was: {content[:500]}")
            raise RuntimeError("Invalid text generation response") from exc


async def call_image(theme: str, keywords: str) -> str:
    """
    Generate a placeholder image URL.
    Note: OpenRouter's Gemini models are for image understanding, not generation.
    This returns a colored placeholder for now. 
    TODO: Integrate with an actual image generation API (DALL-E, Stable Diffusion, etc.)
    """
    logger.info(f"Generating placeholder image for theme: {theme}")
    
    # Create a color based on the theme for visual variety
    color_code = abs(hash(theme)) % 0xFFFFFF
    bg_color = f"{color_code:06x}"
    
    # Use a simple placeholder service
    # Format: https://via.placeholder.com/WIDTHxHEIGHT/BGCOLOR/TEXTCOLOR?text=YOUR+TEXT
    text = theme.replace(' ', '+')[:30]  # Limit length
    placeholder_url = f"https://via.placeholder.com/400x300/{bg_color}/ffffff?text={text}"
    
    logger.info(f"Returning placeholder image: {placeholder_url}")
    return placeholder_url


async def generate_pack(theme: str, level: str, keywords: str) -> Tuple[Dict[str, Any], str]:
    text_task = asyncio.create_task(call_text(theme, level, keywords))
    image_task = asyncio.create_task(call_image(theme, keywords or ""))

    text_json, image_url = await asyncio.gather(text_task, image_task)
    return text_json, image_url
